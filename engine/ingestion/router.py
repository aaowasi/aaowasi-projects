from __future__ import annotations

import csv
import hashlib
import io
import json
import mimetypes
import os
import tempfile
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MAX_BYTES = int(os.environ.get("GRC_MAX_INGEST_BYTES", str(25 * 1024 * 1024)))
TEXT_SUFFIXES = {".txt", ".md", ".yaml", ".yml", ".rego", ".py", ".js", ".ts", ".html", ".css"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_zip_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    safe: list[zipfile.ZipInfo] = []
    total = 0
    for item in archive.infolist():
        member = Path(item.filename)
        if member.is_absolute() or ".." in member.parts:
            raise ValueError(f"Unsafe ZIP path: {item.filename}")
        total += item.file_size
        if total > MAX_BYTES * 4:
            raise ValueError("Expanded ZIP exceeds the configured safety limit")
        safe.append(item)
    return safe


def _approved_url(url: str, allowed: set[str]) -> None:
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.hostname not in allowed
            or parsed.username is not None or parsed.password is not None):
        raise PermissionError("URL ingestion requires an approved HTTPS host without embedded credentials.")


class _AllowlistedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed: set[str]):
        super().__init__()
        self.allowed = allowed

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # urllib follows redirects automatically; the original host allowlist must
        # also apply to every redirect destination before making a new request.
        _approved_url(urllib.parse.urljoin(req.full_url, newurl), self.allowed)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _read_url(url: str) -> tuple[bytes, str]:
    allowed = {host.strip() for host in os.environ.get("GRC_URL_ALLOWLIST", "").split(",") if host.strip()}
    _approved_url(url, allowed)
    request = urllib.request.Request(url, headers={"User-Agent": "grc-assurance-engine/2.0"})
    opener = urllib.request.build_opener(_AllowlistedRedirect(allowed))
    with opener.open(request, timeout=20) as response:
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Remote payload exceeds the configured safety limit")
        return data, response.headers.get_content_type()


def ingest(source: str) -> dict[str, Any]:
    if source.startswith(("https://", "http://")):
        raw, mime = _read_url(source)
        name = Path(urllib.parse.urlparse(source).path).name or "remote-payload"
    else:
        path = Path(source).resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        if path.stat().st_size > MAX_BYTES:
            raise ValueError("Payload exceeds the configured safety limit")
        raw = path.read_bytes()
        name = path.name
        mime = mimetypes.guess_type(name)[0] or "application/octet-stream"

    suffix = Path(name).suffix.lower()
    payload: dict[str, Any] = {
        "source_ref": source,
        "name": name,
        "mime_type": mime,
        "size_bytes": len(raw),
        "sha256": _hash(raw),
        "ingested_at": _now(),
        "parser": "metadata-only",
        "content": None,
        "operations_request": None,
    }
    if suffix == ".json":
        payload.update(parser="json", content=json.loads(raw.decode("utf-8")))
    elif suffix == ".csv":
        payload.update(parser="csv", content=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))))
    elif suffix in TEXT_SUFFIXES:
        payload.update(parser="text", content=raw.decode("utf-8", errors="replace"))
    elif suffix == ".zip":
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            members = _safe_zip_members(archive)
            payload.update(parser="zip-index", content=[{"path": m.filename, "size": m.file_size, "compressed_size": m.compress_size} for m in members])
    elif suffix == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(raw))
            payload.update(parser="pypdf", content={"pages": len(reader.pages), "text": "\n".join((p.extract_text() or "") for p in reader.pages)})
        except ImportError:
            payload["operations_request"] = "Install the optional document adapter: pip install '.[documents]'"
    elif suffix in {".mp3", ".wav", ".m4a", ".mp4", ".mov", ".mkv"}:
        payload["operations_request"] = "Provide an authorized transcript or configure an approved local transcription adapter; raw media is not sent to a third party by default."
    return payload


def ingest_many(sources: list[str]) -> list[dict[str, Any]]:
    results = []
    for source in sources:
        try:
            results.append(ingest(source))
        except Exception as exc:
            results.append({"source_ref": source, "state": "ERROR", "error": str(exc), "ingested_at": _now()})
    return results
