from __future__ import annotations
import hashlib, json, os, pathlib, tarfile
from datetime import datetime, timezone
ROOT = pathlib.Path(__file__).resolve().parents[1]
STAGE = ROOT / ".evidence-staging"
DIST = ROOT / ".evidence-dist"
DIST.mkdir(exist_ok=True)
files = sorted(p for p in STAGE.glob("*.json") if p.is_file())
manifest = {
    "schema": "grc-evidence-manifest/1.0",
    "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "repository": os.environ.get("GITHUB_REPOSITORY", "local"),
    "commit": os.environ.get("GITHUB_SHA", "local-uncommitted"),
    "hash_algorithm": "sha256",
    "files": [],
}
for p in files:
    b = p.read_bytes()
    manifest["files"].append({"name": p.name, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
manifest_path = DIST / "manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
archive = DIST / "raw-evidence.tar.gz"
with tarfile.open(archive, "w:gz") as t:
    for p in files:
        t.add(p, arcname=p.name)
    t.add(manifest_path, arcname="manifest.json")
archive_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
print(json.dumps({"archive": str(archive), "sha256": archive_hash, "files": len(files)}))
