from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class ControlState(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_CONFIGURED = "NOT_CONFIGURED"
    ERROR = "ERROR"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class RiskLevel(StrEnum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"


@dataclass(frozen=True)
class FrameworkDecision:
    framework_id: str
    name: str
    version: str
    selected: bool
    confidence: str
    rationale: list[str]
    legal_review_required: bool = False
    source_url: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    source_type: str
    source_ref: str
    observed_at: str
    sha256: str
    classification: str = "INTERNAL"
    freshness_days: int | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ControlResult:
    control_id: str
    title: str
    state: ControlState
    risk: RiskLevel
    reason: str
    frameworks: list[str]
    evidence_ids: list[str] = field(default_factory=list)
    owner: str = "Unassigned"
    remediation: str = ""
    due_days: int | None = None
    test_type: str = "automated"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["state"] = self.state.value
        payload["risk"] = self.risk.value
        return payload
