from html import escape as e
from pathlib import Path
import json,re,shutil

def render_domains(root):
 data=json.loads((root/'content/projects.json').read_text());catalog=json.loads((root/'content/suite-catalog.json').read_text());cards=[]
 for p in data:
  slug=p['slug'];url='/work/'+slug+'/'
  cards.append('<article class="card" data-project data-domain="'+e(p['domain'],quote=True)+'" data-type="'+e(p['type'],quote=True)+'"><div class="visual"><span>'+e(p['id'])+'</span></div><p class="eyebrow">'+e(p['domain'])+'</p><h3><a href="'+url+'">'+e(p['title'])+'</a></h3><p>'+e(p['summary'])+'</p><p class="chips">'+e(' · '.join(p['frameworks']))+'</p><div class="actions"><a href="'+url+'">Explore work →</a><a href="'+e(p['liveUrl'])+'">Open workflow ↗</a></div></article>')
  links=lambda items:''.join('<li><a href="/work/'+x+'/">'+e(next(q['title'] for q in data if q['slug']==x))+' →</a></li>' for x in items)
  plan='<section class="section content"><h2>Framework anchors</h2><p>'+e(' · '.join(p['frameworks']))+'</p><p>Confirm jurisdiction, applicability, evidence scope and reporting period before assessing conformity.</p></section><section class="section content"><h2>Upstream dependencies</h2><ul>'+links(p['upstream'])+'</ul></section><section class="section content"><h2>Downstream impacts</h2><ul>'+links(p['downstream'])+'</ul></section><section class="section content"><h2>Working review and evidence</h2><p>Use the dedicated domain perspective to maintain '+e(p['entity'])+' records. Record domain ownership, link control tests and evidence, and review the resulting dependencies. Shared record references retain relationships across domains.</p><a href="'+e(p['liveUrl'])+'">Open '+e(p['title'])+' workspace →</a><p>Public tools recalculate locally. External telemetry collection requires authorized production integration.</p></section>'
  t=(root/'templates/project.html').read_text()
  vals={'LIVE':e(p['liveUrl']),'PLAN_SECTIONS':plan,'TITLE':e(p['title']),'ID':p['id'],'DOMAIN':e(p['domain']),'SUMMARY':e(p['summary']),'PURPOSE':e(p['outcome']),'BASIS':e(p['evidenceBasis']),'CODE':e(p['codeUrl']),'SLUG':slug,'SOURCE':e(p['sourcePath']),'CAPABILITIES':''.join('<li>'+e(x)+'</li>' for x in p['capabilities']),'OUTPUTS':''.join('<li>'+e(x)+'</li>' for x in p['outputs']),'GUARDRAILS':''.join('<li>'+e(x)+'</li>' for x in p['guardrails'])}
  for k,v in vals.items():t=t.replace('{{'+k+'}}',v)
  path=root/'site/work'/slug/'index.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(t)
 t=(root/'templates/gallery.html').read_text().replace('{{PROJECT_CARDS}}',''.join(cards)).replace('{{DOMAINS}}',''.join('<option>'+e(p['domain'])+'</option>' for p in data)).replace('{{TYPES}}','<option>Connected governance workflow</option>');t=t.replace('10 projects',str(len(data))+' projects');(root/'site/index.html').write_text(t)
 (root/'site/data/projects.json').write_text(json.dumps(data,indent=2)+'\n')
 for route,template in [('suite','suite'),('workspace','domain-workspace')]:
  t=(root/'templates'/ (template+'.html')).read_text()
  for k,v in {'DOMAIN_COUNT':len(data),'ENTITY_COUNT':len(catalog['entities']),'VIEW_COUNT':len(catalog['views'])}.items():t=t.replace('{{'+k+'}}',str(v))
  dest=root/'site'/route/'index.html';dest.parent.mkdir(exist_ok=True);dest.write_text(t)
 (root/'site/data/evaluation-domains.json').write_text(json.dumps([p['domain'] for p in data],indent=2)+'\n')
 print('Generated',len(data),'dedicated domain projects')
