"""Render recorded public workflow evidence without interpreting it as client impact."""
from datetime import datetime
from html import escape
import re
from urllib.parse import urlsplit

def timestamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Evidence timestamps require a timezone')
    return parsed

def render(snapshot):
    as_of = timestamp(snapshot['retrievedAt'])
    rows = []
    success = 0
    total = 0
    repositories = snapshot['repositories']
    for repo in repositories:
        name, commit = repo['repository'], repo['commit']
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', name) or not re.fullmatch(r'[a-f0-9]{40}', commit):
            raise ValueError('Invalid repository or commit')
        count = 0
        for run in repo['runs']:
            if run['commit'] != commit:
                raise ValueError('Run commit does not match observed commit')
            created, updated = timestamp(run['createdAt']), timestamp(run['updatedAt'])
            if updated < created or updated > as_of:
                raise ValueError('Invalid workflow observation interval')
            url = urlsplit(run['url'])
            if url.scheme != 'https' or url.netloc != 'github.com' or not re.fullmatch('/'+re.escape(name)+r'/actions/runs/[0-9]+', url.path) or url.query or url.fragment:
                raise ValueError('Invalid workflow evidence URL')
            passed = run['status'] == 'completed' and run['conclusion'] == 'success'
            success += int(passed)
            count += int(passed)
            total += 1
            elapsed = (updated-created).total_seconds()
            cells = [name, run['name'], run['status'], run['conclusion'] or 'Pending', run['createdAt'], run['updatedAt'], f'{elapsed:g} seconds']
            rows.append('<tr>'+''.join('<td>'+escape(str(v))+'</td>' for v in cells)+'<td><a href="'+escape(run['url'],quote=True)+'">View run ↗</a></td></tr>')
        repo['_successful_checks'] = count
    headings = ['Repository','Workflow','Status','Conclusion','Created (UTC)','Updated (UTC)','Workflow elapsed','Source']
    commits = ''.join('<li><strong>'+escape(r['repository'])+'</strong>: '+str(r['_successful_checks'])+' successful checks / '+str(len(r['runs']))+' observed. Commit <a href="https://github.com/'+escape(r['repository'])+'/commit/'+r['commit']+'"><code>'+r['commit']+'</code></a></li>' for r in repositories)
    return '<p class="eyebrow">Actual public records / Snapshot as of '+escape(snapshot['retrievedAt'])+'</p><h2>Recorded workflow checks.</h2><p class="lead">'+str(success)+' successful workflow checks across '+str(len(repositories))+' repositories, from '+str(total)+' observed runs at the commits below.</p><p>These are recorded GitHub Actions results for this portfolio. They show the named workflow checks completed successfully at a particular commit. They do not measure client outcomes, audit completion, control effectiveness or commercial ROI.</p><ul>'+commits+'</ul><div class="table-scroll" role="region" tabindex="0" aria-label="Observed GitHub Actions runs"><table><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headings)+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table></div><h2>How to read the evidence</h2><p>Workflow elapsed = updatedAt − createdAt. It includes queueing and GitHub workflow lifecycle time; it is not audit duration, reviewer effort or isolated test execution time. These observations are not an uptime sample, all-time pass rate or current live status.</p><p>The snapshot is checked into source and rendered during the static build. Publishing a later change does not silently move these results to the new commit. Open each source run to inspect its logs, workflow definition and exact coverage.</p><p>The recorded site runs predate the change that adds JavaScript core tests to site CI. They must not be used as evidence that those earlier runs executed the core tests. Local core-test results are separate from these public workflow observations.</p><div class="actions"><a class="button" href="/data/verified-delivery.json">Download recorded source JSON</a><a href="https://github.com/aaowasi/aaowasi-projects/blob/main/docs/DELIVERY-EVIDENCE.md">Read provenance & refresh procedure ↗</a><a href="/workspace/">Open the workspace ↗</a></div>'
