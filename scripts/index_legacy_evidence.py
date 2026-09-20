from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a migration manifest for historical evidence without copying the source files")
    parser.add_argument("source", help="directory containing historical evidence")
    parser.add_argument("--output", default="legacy-baseline-manifest.json")
    args = parser.parse_args()
    source = Path(args.source).resolve()
    if not source.is_dir():
        parser.error("source must be a directory")
    files = []
    for path in sorted(item for item in source.rglob("*") if item.is_file()):
        files.append({
            "path": path.relative_to(source).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": digest(path),
            "disposition": "retain_in_private_or_approved_baseline_release",
        })
    payload = {
        "schema": "grc-legacy-evidence-manifest/v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_root": source.name,
        "file_count": len(files),
        "files": files,
        "publication_warning": "Classify and approve every source before publication. Use private storage for client or regulated data.",
    }
    output = Path(args.output)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
