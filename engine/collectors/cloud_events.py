from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

SENSITIVE_KEYS = {"authorization", "token", "secret", "password", "credential", "cookie"}


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: "[REDACTED]" if key.lower() in SENSITIVE_KEYS else _redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def normalize_jsonl(path: str | Path, allowed_event_types: Iterable[str] = ()) -> dict[str, Any]:
    """Normalize JSONL security events, redact common secrets, and report malformed records."""
    source = Path(path)
    allow = set(allowed_event_types)
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for line_number, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
            event_type = str(event.get("event_type", event.get("eventName", "unknown")))
            if allow and event_type not in allow:
                continue
            accepted.append(_redact(event))
        except (json.JSONDecodeError, AttributeError) as exc:
            rejected.append({"line": line_number, "reason": str(exc)})
    types = Counter(str(event.get("event_type", event.get("eventName", "unknown"))) for event in accepted)
    return {
        "source": str(source), "accepted": len(accepted), "rejected": rejected,
        "event_type_counts": dict(types), "events": accepted,
        "control_mappings": ["SOC2-CC7.2", "ISO27001-A.8.15", "NIST-CSF-DE.CM"],
    }
