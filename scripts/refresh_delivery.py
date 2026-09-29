"""Explicit manual refresh of public runs for the already pinned commits. No token required."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
ROOT = Path(__file__).resolve().parents[1]
path = ROOT/'content/verified-delivery.json'
old = json.loads(path.read_text())
repositories = []
for repo in old['repositories']:
    url = 'https://api.github.com/repos/'+repo['repository']+'/actions/runs?'+urlencode({'head_sha':repo['commit'],'per_page':100})
    with urlopen(Request(url, headers={'Accept':'application/vnd.github+json','User-Agent':'AAO-evidence-refresh'}), timeout=30) as response:
        runs = json.load(response)['workflow_runs']
    selected = []
    for name in dict.fromkeys(r['name'] for r in repo['runs']):
        matches = [r for r in runs if r['name']==name and r['head_sha']==repo['commit']]
        if not matches:
            raise ValueError('No matching run for '+repo['repository']+' / '+name)
        r = max(matches, key=lambda x:x['id'])
        selected.append({'name':r['name'],'status':r['status'],'conclusion':r['conclusion'],'createdAt':r['created_at'],'updatedAt':r['updated_at'],'url':r['html_url'],'commit':r['head_sha']})
    repositories.append({'repository':repo['repository'],'commit':repo['commit'],'runs':selected})
snapshot = {'retrievedAt':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'sourceType':'GitHub Actions public workflow records','repositories':repositories}
from build_delivery import render
render(json.loads(json.dumps(snapshot)))
path.write_text(json.dumps(snapshot,indent=2)+'\n')
print('Refreshed pinned-commit observations. Review the JSON diff, build, test and commit explicitly.')
