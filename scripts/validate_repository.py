from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


json_files = sorted(ROOT.rglob("*.json"))
for path in json_files:
    if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
        continue
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

manifests = sorted((ROOT / "projects").glob("*/manifest.json"))
require(len(manifests) == 10, f"expected 10 project manifests, found {len(manifests)}")
ids = []
for path in manifests:
    item = json.loads(path.read_text(encoding="utf-8"))
    ids.append(item.get("project_id"))
    for key in ["name", "purpose", "framework_candidates", "capabilities", "telemetry_sources", "outputs", "guardrails"]:
        require(bool(item.get(key)), f"{path.relative_to(ROOT)} missing {key}")
require(ids == [f"P{i:02d}" for i in range(1, 11)], f"project IDs are not P01-P10 in order: {ids}")

for path in (ROOT / "oscal").rglob("*.json"):
    data = json.loads(path.read_text(encoding="utf-8"))
    metadata = data.get("component-definition", {}).get("metadata", {})
    require(metadata.get("oscal-version") == "1.2.3", f"{path.relative_to(ROOT)} must target OSCAL 1.2.3")

if errors:
    print("REPOSITORY VALIDATION FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print(f"validated {len(json_files)} JSON files and {len(manifests)} project manifests")
