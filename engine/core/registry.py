from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import FrameworkDecision

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "config" / "framework-registry.json"


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _path_value(context: dict[str, Any], dotted: str) -> Any:
    value: Any = context
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def _condition_matches(context: dict[str, Any], condition: dict[str, Any]) -> bool:
    actual = _path_value(context, condition["field"])
    if "equals" in condition:
        return actual == condition["equals"]
    if "contains_any" in condition:
        values = actual if isinstance(actual, list) else [actual]
        return any(item in values for item in condition["contains_any"])
    if "present" in condition:
        return (actual not in (None, "", [], {})) is bool(condition["present"])
    raise ValueError(f"Unsupported registry condition: {condition}")


def select_frameworks(context: dict[str, Any], registry: dict[str, Any] | None = None) -> list[FrameworkDecision]:
    registry = registry or load_registry()
    decisions: list[FrameworkDecision] = []
    requested = set(context.get("requested_frameworks", []))
    for item in registry["frameworks"]:
        reasons: list[str] = []
        matched = 0
        for rule in item.get("applicability", []):
            if _condition_matches(context, rule):
                matched += 1
                reasons.append(rule["reason"])
        if item["id"] in requested:
            matched += 2
            reasons.append("Explicitly requested by the assessment owner")
        selected = matched >= item.get("minimum_matches", 1)
        confidence = "HIGH" if matched >= 2 else "MEDIUM" if matched == 1 else "LOW"
        decisions.append(
            FrameworkDecision(
                framework_id=item["id"],
                name=item["name"],
                version=item["version"],
                selected=selected,
                confidence=confidence,
                rationale=reasons or ["No configured applicability signal matched"],
                legal_review_required=item.get("legal_review_required", False),
                source_url=item.get("source_url", ""),
            )
        )
    return decisions


def selected_framework_ids(context: dict[str, Any]) -> list[str]:
    return [d.framework_id for d in select_frameworks(context) if d.selected]
