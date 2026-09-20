from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import ControlResult, ControlState, RiskLevel
from .registry import select_frameworks

ROOT = Path(__file__).resolve().parents[2]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _get(data: dict[str, Any], dotted: str) -> Any:
    value: Any = data
    for key in dotted.split("."):
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def _evaluate_rule(rule: dict[str, Any], evidence: dict[str, Any], selected: set[str]) -> ControlResult:
    applicable = set(rule.get("frameworks", [])) & selected
    if rule.get("frameworks") and not applicable:
        state = ControlState.NOT_APPLICABLE
        reason = "No selected framework or context requires this test"
    elif rule.get("manual_review", False):
        state = ControlState.MANUAL_REVIEW
        reason = rule.get("manual_reason", "Qualified human judgment is required")
    else:
        value = _get(evidence, rule["evidence_path"])
        if value is None:
            state = ControlState.NOT_CONFIGURED
            reason = f"Evidence path is unavailable: {rule['evidence_path']}"
        else:
            operator = rule["operator"]
            expected = rule.get("expected")
            try:
                if operator == "equals":
                    passed = value == expected
                elif operator == "not_equals":
                    passed = value != expected
                elif operator == "less_than_or_equal":
                    passed = value <= expected
                elif operator == "greater_than_or_equal":
                    passed = value >= expected
                elif operator == "contains":
                    passed = expected in value
                else:
                    raise KeyError(f"Unsupported operator: {operator}")
            except (KeyError, TypeError) as exc:
                return ControlResult(
                    control_id=rule["id"], title=rule["title"], state=ControlState.ERROR,
                    risk=RiskLevel(rule.get("risk", "MODERATE")), reason=f"Evaluation error: {exc}",
                    frameworks=rule.get("frameworks", []), owner=rule.get("owner", "Unassigned"),
                    remediation=rule.get("remediation", "Review rule configuration"), due_days=rule.get("due_days"),
                )
            state = ControlState.PASS if passed else ControlState.FAIL
            reason = rule.get("pass_reason", "Expected condition observed") if passed else rule.get("fail_reason", f"Expected {operator} {expected!r}; observed {value!r}")
    return ControlResult(
        control_id=rule["id"], title=rule["title"], state=state,
        risk=RiskLevel(rule.get("risk", "MODERATE")), reason=reason,
        frameworks=rule.get("frameworks", []), evidence_ids=rule.get("evidence_ids", []),
        owner=rule.get("owner", "Unassigned"), remediation=rule.get("remediation", ""),
        due_days=rule.get("due_days"), test_type="manual" if rule.get("manual_review") else "automated",
    )


def run_assessment(context: dict[str, Any], evidence: dict[str, Any], controls_path: Path | None = None) -> dict[str, Any]:
    controls_path = controls_path or ROOT / "config" / "control-tests.json"
    controls = json.loads(controls_path.read_text(encoding="utf-8"))["controls"]
    framework_decisions = select_frameworks(context)
    selected = {d.framework_id for d in framework_decisions if d.selected}
    results = [_evaluate_rule(rule, evidence, selected) for rule in controls]
    counts = Counter(result.state.value for result in results)
    tested = counts[ControlState.PASS.value] + counts[ControlState.FAIL.value]
    score = round(100 * counts[ControlState.PASS.value] / tested, 1) if tested else None
    return {
        "assessment_id": context.get("assessment_id", "assessment-demo"),
        "generated_at": _now(),
        "scope": {"organization": context.get("organization", {}), "selected_frameworks": sorted(selected)},
        "framework_decisions": [d.to_dict() for d in framework_decisions],
        "summary": {"counts": {state.value: counts[state.value] for state in ControlState}, "effectiveness_score": score, "scoring_note": "Score uses PASS/(PASS+FAIL); excluded states remain visible and are never silently treated as passes."},
        "results": [result.to_dict() for result in results],
        "limitations": [
            "This reference engine scopes and tests configured controls; it does not issue certification, audit opinions, or legal advice.",
            "Legal applicability and subjective effectiveness judgments are routed to MANUAL_REVIEW.",
        ],
    }
