from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else [value]


def _is_wildcard_admin(statement: dict[str, Any]) -> bool:
    if statement.get("Effect") != "Allow":
        return False
    actions = _items(statement.get("Action", []))
    resources = _items(statement.get("Resource", []))
    return "*" in actions and "*" in resources


def analyze_iam_export(path: str | Path) -> dict[str, Any]:
    """Normalize an exported IAM policy bundle without requiring live AWS credentials."""
    source = Path(path)
    payload = json.loads(source.read_text(encoding="utf-8"))
    policies = payload.get("policies", [])
    violations: list[dict[str, str]] = []
    for policy in policies:
        statements = _items(policy.get("document", {}).get("Statement", []))
        for index, statement in enumerate(statements):
            if isinstance(statement, dict) and _is_wildcard_admin(statement):
                violations.append({"policy": policy.get("name", "unnamed"), "statement": str(index), "reason": "Allow Action=* Resource=*"})
    return {
        "source": str(source),
        "policy_count": len(policies),
        "wildcard_admin_count": len(violations),
        "violations": violations,
        "control_mappings": ["SOC2-CC6.1", "ISO27001-A.5.15", "ISO27001-A.8.2", "NIST-CSF-PR.AA"],
    }
