from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def run_diagnostics() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, remediation: str = "") -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "remediation": "" if ok else remediation})

    for rel in ["config/framework-registry.json", "config/control-tests.json", "schemas/client-context.schema.json"]:
        path = ROOT / rel
        try:
            json.loads(path.read_text(encoding="utf-8"))
            add(f"valid_json:{rel}", True)
        except Exception as exc:
            add(f"valid_json:{rel}", False, f"Repair JSON syntax: {exc}")
    add("python>=3.11", True)
    add("opa_available", shutil.which("opa") is not None, "Install OPA 1.20.2 or run it through Docker Compose")
    add("mcp_sdk_available", importlib.util.find_spec("mcp") is not None, "Install optional dependency: pip install 'mcp>=2,<3'")
    failed = sum(item["status"] == "FAIL" for item in checks)
    return {
        "status": "READY" if failed == 0 else "ACTION_REQUIRED",
        "checks": checks,
        "operations_permission_action_brief": None if failed == 0 else {
            "blocked_capability": "One or more optional or required runtime checks failed",
            "owner_action": [item["remediation"] for item in checks if item["status"] == "FAIL"],
            "resume_command": "python -m engine.cli diagnostics",
        },
    }
