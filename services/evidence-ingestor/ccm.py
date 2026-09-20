from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from engine.assurance.reporting import write_report
from engine.core.assessment import run_assessment

STAGE = ROOT / ".evidence-staging"
RUNTIME = ROOT / "data" / "runtime"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def github_get(path: str) -> tuple[str, Any]:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not repo:
        return "NOT_CONFIGURED", {"reason": "GITHUB_REPOSITORY is not set"}
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "grc-assurance-engine/2.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com/repos/{repo}{path}", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return "COLLECTED", json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read(2000).decode("utf-8", errors="replace")
        return "ERROR", {"http_status": exc.code, "body": body}
    except Exception as exc:
        return "ERROR", {"error": str(exc)}


def collect() -> dict[str, Any]:
    STAGE.mkdir(exist_ok=True)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    base = {}  # Missing real evidence remains NOT_CONFIGURED; never seed with demo signals.
    state, repository = github_get("")
    raw = {"collector": "github_repository", "state": state, "observed_at": now(), "payload": repository}
    (STAGE / "github-repository.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
    base["collector_health"] = {"github_repository": state}
    base["provenance"] = {"github_repository_sha256": digest(repository)}
    (RUNTIME / "evidence-signals.json").write_text(json.dumps(base, indent=2), encoding="utf-8")
    return base


def main() -> int:
    context_path = Path(os.environ.get("GRC_CLIENT_CONTEXT", ROOT / "examples" / "client-context-saas-ai-eu.json"))
    context = json.loads(context_path.read_text(encoding="utf-8"))
    assessment = run_assessment(context, collect())
    write_report(assessment, RUNTIME / "control-status.json")
    write_report(assessment, ROOT / "reports" / "assurance-report.md")
    (STAGE / "assessment-results.json").write_text(json.dumps(assessment, indent=2), encoding="utf-8")
    print(json.dumps(assessment["summary"]))
    return 1 if assessment["summary"]["counts"]["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
