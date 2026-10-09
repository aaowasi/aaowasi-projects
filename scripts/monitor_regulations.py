"""Daily **source-change signal** for a bounded, curated set of official pages.

A content fingerprint is not a legal-change detector, compliance opinion or authorization.
Only human reviewers determine applicability, effective dates and mapping changes.
No login, secret, credential, cookies or personal data are collected.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "content/regulatory-sources.json"
OBSERVATION_PATH = ROOT / "content/regulatory-observations.json"
ALLOWED_HOSTS = frozenset({
    "ai-act-service-desk.ec.europa.eu",
    "www.edpb.europa.eu",
    "ico.org.uk",
    "www.nist.gov",
    "www.imda.gov.sg",
})
MAX_BYTES = 1_000_000
TIMEOUT_SECONDS = 12


def check_url(url):
    p = urlsplit(url)
    if (p.scheme != "https" or p.username or p.password
            or p.port not in (None, 443) or p.hostname not in ALLOWED_HOSTS):
        raise ValueError("Only the approved HTTPS regulator/source origins are allowed.")
    return url


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # No redirects to third-party hosts, protocols or internal networks.
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.omit = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "svg"}:
            self.omit += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "svg"}:
            self.omit = max(0, self.omit - 1)

    def handle_data(self, data):
        if not self.omit:
            self.data.append(data)


def fingerprint(payload):
    if len(payload) > MAX_BYTES:
        raise ValueError("Official page response exceeds 1 MB safety limit.")
    # Visible text is a change signal, not authenticated legal text.
    doc = VisibleText()
    doc.feed(payload.decode("utf-8", errors="replace"))
    text = re.sub(r"\s+", " ", " ".join(doc.data)).strip()
    if len(text) < 100:
        raise ValueError("Source page has insufficient readable content.")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch_source(url):
    check_url(url)
    req = Request(url, headers={
        "User-Agent": "AAO-Regulatory-Source-Observer/1.0 (public source metadata)",
        "Accept": "text/html, application/xhtml+xml;q=0.9",
    })
    opener = build_opener(SafeRedirect())
    with opener.open(req, timeout=TIMEOUT_SECONDS) as response:
        final = response.geturl()
        check_url(final)
        if "html" not in response.headers.get("Content-Type", "").lower():
            raise ValueError("Official source did not return an HTML document.")
        payload = response.read(MAX_BYTES + 1)
    return fingerprint(payload)


def observe(registry, previous, fetcher=fetch_source, observed_at=None):
    if registry.get("version") != 1 or not isinstance(registry.get("sources"), list):
        raise ValueError("Expected curated regulatory source register v1.")
    seen = set()
    prior = {x["url"]: x for x in previous.get("entries", [])
             if isinstance(x, dict) and isinstance(x.get("url"), str)}
    now = observed_at or datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    entries = []
    for source in registry["sources"]:
        url = check_url(source["url"])
        if url in seen:
            raise ValueError("Duplicate curated regulatory source URL.")
        seen.add(url)
        past = prior.get(url, {})
        entry = {
            "url": url,
            "jurisdiction": source["jurisdiction"],
            "title": source["title"],
            "domainSlugs": source["domainSlugs"],
            "fingerprint": past.get("fingerprint"),
            "previousFingerprint": past.get("previousFingerprint"),
            "firstSeenAt": past.get("firstSeenAt"),
            "lastSuccessfulAt": past.get("lastSuccessfulAt"),
            "lastCheckedAt": now,
            "changeDetectedAt": past.get("changeDetectedAt"),
            "reviewState": past.get("reviewState", "not_checked"),
            "fetchStatus": "unavailable",
            "detail": None,
        }
        try:
            current = fetcher(url)
            if not re.fullmatch(r"[a-f0-9]{64}", current):
                raise ValueError("Invalid content fingerprint from fetcher.")
            entry["fetchStatus"] = "observed"
            entry["lastSuccessfulAt"] = now
            if not past.get("fingerprint"):
                entry.update(fingerprint=current, firstSeenAt=now, reviewState="baseline")
            elif current != past["fingerprint"]:
                # Keep the *original* baseline and pending review until a person
                # resolves it; a recurring fetch must not silently approve changes.
                if past.get("reviewState") != "change_pending_review":
                    entry["previousFingerprint"] = past["fingerprint"]
                    entry["changeDetectedAt"] = now
                entry["fingerprint"] = current
                entry["reviewState"] = "change_pending_review"
            else:
                # A previously flagged change stays unreviewed after a stable fetch.
                entry["reviewState"] = ("change_pending_review"
                                        if past.get("reviewState") == "change_pending_review"
                                        else "baseline")
        except (OSError, HTTPError, URLError, ValueError, UnicodeError) as ex:
            # Never erase a previous baseline or pending review on a network fault.
            entry["detail"] = type(ex).__name__ + ": unable to verify source content"
            entry["reviewState"] = past.get("reviewState", "not_checked")
        entries.append(entry)
    return {
        "version": 1,
        "generatedAt": now,
        "scope": "Curated official-source page-change indicators only; no automated legal interpretation",
        "entries": entries,
    }


def main():
    registry = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    previous = json.loads(OBSERVATION_PATH.read_text(encoding="utf-8"))
    result = observe(registry, previous)
    OBSERVATION_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {k: sum(x["reviewState"] == k for x in result["entries"])
              for k in ["change_pending_review", "baseline", "not_checked"]}
    unavailable = sum(x["fetchStatus"] != "observed" for x in result["entries"])
    line = ("Curated source watch: " + str(len(result["entries"])) + " checked; "
            + str(unavailable) + " unavailable; " + str(counts["change_pending_review"])
            + " pending human review. Source changes do not imply new law.")
    print(line)
    if __name__ == "__main__" and "GITHUB_STEP_SUMMARY" in __import__("os").environ:
        with open(__import__("os").environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("## Curated regulatory page changes\n\n" + line + "\n\n")
            for entry in result["entries"]:
                f.write("- " + entry["title"] + ": **" + entry["reviewState"]
                        + "** (fetch: " + entry["fetchStatus"] + ")\n")
            f.write("\nA reviewer must verify the legal text, applicability and effective date.\n")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print("Regulatory source watch failed without mutating the state: " + str(exc), file=sys.stderr)
        sys.exit(1)
