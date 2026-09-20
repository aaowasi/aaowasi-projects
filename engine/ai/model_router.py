from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModelCandidate:
    provider: str
    model_id: str
    context_length: int
    input_cost: float
    output_cost: float
    local: bool


def discover_candidates(task: str, data_classification: str = "PUBLIC") -> list[ModelCandidate]:
    """Discover eligible helpers. Assurance decisions remain deterministic and human-reviewable."""
    mode = os.environ.get("GRC_AI_MODE", "disabled")
    if mode == "disabled":
        return []
    if mode == "local":
        return [ModelCandidate("ollama", os.environ.get("OLLAMA_MODEL", "configured-local-model"), 0, 0.0, 0.0, True)]
    if mode != "openrouter-free" or data_classification != "PUBLIC":
        return []
    request = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={"User-Agent": "grc-assurance-engine/2.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        models: dict[str, Any] = json.load(response)
    candidates = []
    for item in models.get("data", []):
        pricing = item.get("pricing", {})
        try:
            prompt = float(pricing.get("prompt", "1"))
            completion = float(pricing.get("completion", "1"))
        except ValueError:
            continue
        if prompt == 0 and completion == 0:
            candidates.append(ModelCandidate("openrouter", item["id"], int(item.get("context_length") or 0), 0.0, 0.0, False))
    return sorted(candidates, key=lambda model: (model.context_length, model.model_id), reverse=True)


def select_model(task: str, data_classification: str = "PUBLIC") -> dict[str, Any]:
    candidates = discover_candidates(task, data_classification)
    if not candidates:
        return {
            "state": "NOT_CONFIGURED",
            "reason": "No authorized zero-cost model is available. The deterministic assurance pipeline continues without LLM assistance.",
            "guarantee": "Free endpoints, model quality, global availability, and zero downtime cannot be guaranteed.",
        }
    selected = candidates[0]
    return {"state": "SELECTED", **selected.__dict__, "use_boundary": "Drafting and classification assistance only; never the final compliance, legal, or audit conclusion."}
