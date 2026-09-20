from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Literal

from mcp.server import MCPServer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from engine.core.assessment import run_assessment
from engine.core.registry import select_frameworks

RISK_FILE = ROOT / "data" / "source" / "risk-register.json"
VENDOR_FILE = ROOT / "data" / "source" / "vendors.json"
mcp = MCPServer("grc-ai-governance-engine")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def public_record(row: dict) -> dict:
    blocked = {"contact_email", "contract_url", "raw_evidence", "secret", "token"}
    return {key: value for key, value in row.items() if key not in blocked}


@mcp.tool()
def list_risks(status: str = "") -> list[dict]:
    """Return sanitized risk-register records, optionally filtered by status."""
    rows = load(RISK_FILE)
    return [public_record(row) for row in rows if not status or row.get("status") == status]


@mcp.tool()
def get_vendor(vendor_id: str) -> dict:
    """Return sanitized vendor and fourth-party dependency context."""
    for vendor in load(VENDOR_FILE):
        if vendor.get("id") == vendor_id:
            return public_record(vendor)
    return {"error": "vendor_not_found", "vendor_id": vendor_id}


@mcp.tool()
def evaluate_vendor(vendor_id: str, evidence_age_days: int, open_critical_findings: int, fourth_party_concentration: int) -> dict:
    """Run deterministic, non-mutating vendor triage; human approval remains required."""
    vendor = get_vendor(vendor_id)
    if "error" in vendor:
        return vendor
    if min(evidence_age_days, open_critical_findings, fourth_party_concentration) < 0:
        return {"error": "inputs_must_be_non_negative"}
    score = min(25, int(vendor["residual_risk"]) + min(evidence_age_days // 30, 5) + open_critical_findings * 4 + max(fourth_party_concentration - 2, 0) * 2)
    decision: Literal["approve", "approve_with_conditions", "escalate"] = "approve" if score <= 8 else "approve_with_conditions" if score <= 14 else "escalate"
    return {"vendor_id": vendor_id, "score": score, "recommendation": decision, "requires_human_approval": True, "rationale": {"base_residual": vendor["residual_risk"], "evidence_age_days": evidence_age_days, "critical_findings": open_critical_findings, "fourth_party_concentration": fourth_party_concentration}}


@mcp.tool()
def scope_frameworks(context_json: str) -> list[dict]:
    """Return framework applicability candidates and review flags from client context JSON."""
    return [decision.to_dict() for decision in select_frameworks(json.loads(context_json))]


@mcp.tool()
def assess_controls(context_json: str, evidence_json: str) -> dict:
    """Run deterministic control tests without modifying records or approving exceptions."""
    return run_assessment(json.loads(context_json), json.loads(evidence_json))


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    mcp.run(transport="streamable-http") if transport == "streamable-http" else mcp.run()
