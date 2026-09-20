from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def render_markdown(assessment: dict[str, Any]) -> str:
    summary = assessment["summary"]
    scope = assessment["scope"]
    selected = ", ".join(scope["selected_frameworks"]) or "No framework selected"
    rows = []
    for result in assessment["results"]:
        rows.append("| {control_id} | {title} | {state} | {risk} | {reason} | {owner} | {remediation} |".format(**result).replace("\n", " "))
    gaps = [item for item in assessment["results"] if item["state"] in {"FAIL", "ERROR", "NOT_CONFIGURED", "MANUAL_REVIEW"}]
    immediate = [item for item in gaps if item["risk"] in {"CRITICAL", "HIGH"}]
    questions = []
    for item in gaps:
        if item["state"] == "NOT_CONFIGURED":
            questions.append(f"- Provide current evidence for **{item['control_id']} — {item['title']}**.")
        elif item["state"] == "MANUAL_REVIEW":
            questions.append(f"- Assign a qualified reviewer for **{item['control_id']} — {item['title']}** and record the decision basis.")
    return f"""# Enterprise Assurance Report

**Assessment:** {assessment['assessment_id']}  
**Generated:** {assessment['generated_at']}  
**Organization:** {scope.get('organization', {}).get('name', 'Not supplied')}  
**Selected frameworks:** {selected}  
**Effectiveness score:** {summary['effectiveness_score'] if summary['effectiveness_score'] is not None else 'Not scored'}%

## Executive summary

The engine recorded **{summary['counts']['PASS']} pass**, **{summary['counts']['FAIL']} fail**, **{summary['counts']['NOT_CONFIGURED']} not configured**, **{summary['counts']['ERROR']} error**, **{summary['counts']['NOT_APPLICABLE']} not applicable**, and **{summary['counts']['MANUAL_REVIEW']} manual review** results. The score excludes every non-tested state; exclusions remain visible.

## Domain and framework mapping

{chr(10).join(f"- **{d['framework_id']} — {d['name']} ({d['version']}):** {'selected' if d['selected'] else 'not selected'}; {', '.join(d['rationale'])}" for d in assessment['framework_decisions'])}

## Control and gap matrix

| Control ID | Requirement / test | State | Risk | Evidence-based reason | Owner | Remediation |
| --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

## Audit and remediation roadmap

### Immediate / high priority

{chr(10).join(f"- **{item['control_id']} ({item['risk']}):** {item['remediation']} Owner: {item['owner']}. Target: {item.get('due_days') or 'owner-defined'} days." for item in immediate) or '- No critical or high-priority gap was produced by the configured tests.'}

### Follow-through

1. Confirm control ownership and risk acceptance authority.
2. Collect missing evidence through an approved connector or signed upload.
3. Remediate or approve a time-bound exception with rationale.
4. Retest the same deterministic procedure.
5. Publish the evidence bundle, manifest, report, and decision log as a release snapshot.

## Actionable evidence and operations request

{chr(10).join(questions) or '- No additional evidence request was generated.'}

## Limitations

{chr(10).join('- ' + item for item in assessment['limitations'])}
"""


def write_report(assessment: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".json":
        output.write_text(json.dumps(assessment, indent=2), encoding="utf-8")
    else:
        output.write_text(render_markdown(assessment), encoding="utf-8")
