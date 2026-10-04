from pathlib import Path
import json,re
from build_docs import fingerprint
root=Path(__file__).resolve().parents[1]
saved=json.loads((root/'docs-sync.json').read_text());current,_=fingerprint(root)
assert saved['sourceFingerprint']==current,'Documentation is stale. Run scripts/build_site.py and commit docs plus code.'
assert saved['sourceFingerprint'] in (root/'DOCS.md').read_text()
assert '<!-- GENERATED-ARCHITECTURE:START -->' in (root/'README.md').read_text()
projects=json.loads((root/'content/projects.json').read_text());reviews=json.loads((root/'content/domain-reviews.json').read_text())
assert {x['slug'] for x in projects}=={x['slug'] for x in reviews}
for page in (root/'site').rglob('*.html'):
 s=page.read_text()
 assert not re.search(r'https://github.com/(?!aaowasi(?:/|["\s]))',s),str(page)+' external repository reference'
 assert not re.search(r'20\s*</strong>\s*<span>connected workflows|13 GRC operating domains',s),str(page)+' stale count'
 if not (root/'engine').exists():continue
 for href in re.findall(r'href="(/work/[^"#?]+/)',s):assert (root/'site'/href.strip('/')/'index.html').exists(),str(page)+' retired route '+href
for file in ['LICENSE','TERMS_AND_CONDITIONS.md','DOCS.md']:assert (root/file).exists()
print('PASS: source/docs synchronization, native routes, project review contracts and licensing files')
