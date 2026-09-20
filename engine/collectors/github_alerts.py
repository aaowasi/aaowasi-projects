from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

API_VERSION = "2022-11-28"


def _get(repo: str, endpoint: str, token: str) -> tuple[str, list[dict[str, Any]] | dict[str, Any]]:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}{endpoint}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "grc-assurance-engine/2.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return "COLLECTED", json.load(response)
    except urllib.error.HTTPError as exc:
        return "ERROR", {"http_status": exc.code, "reason": exc.reason}
    except Exception as exc:
        return "ERROR", {"reason": str(exc)}


def collect_github_alerts(repo: str | None = None, token: str | None = None) -> dict[str, Any]:
    """Collect open GitHub security alerts using a read-only token; never mutates alerts."""
    repo = repo or os.getenv("GITHUB_REPOSITORY", "")
    token = token or os.getenv("GITHUB_TOKEN", "")
    if not repo or not token:
        return {"state": "NOT_CONFIGURED", "reason": "GITHUB_REPOSITORY and a read-only GITHUB_TOKEN are required"}
    endpoints = {
        "code_scanning": "/code-scanning/alerts?state=open&per_page=100",
        "dependabot": "/dependabot/alerts?state=open&per_page=100",
        "secret_scanning": "/secret-scanning/alerts?state=open&per_page=100",
    }
    result: dict[str, Any] = {"state": "COLLECTED", "repository": repo, "sources": {}, "open_alerts": {}}
    for name, endpoint in endpoints.items():
        state, payload = _get(repo, endpoint, token)
        result["sources"][name] = state
        if state == "COLLECTED" and isinstance(payload, list):
            result["open_alerts"][name] = len(payload)
        else:
            result["open_alerts"][name] = None
            result["state"] = "PARTIAL" if result["state"] == "COLLECTED" else result["state"]
    result["control_mappings"] = ["SOC2-CC6.1", "SOC2-CC7.1", "ISO27001-A.8.8", "NIST-CSF-DE.CM"]
    return result
