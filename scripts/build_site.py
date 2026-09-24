from pathlib import Path
from html import escape as e
from urllib.parse import urlsplit
import json, re, shutil
ROOT=Path(__file__).resolve().parents[1]
IS_PROJECT=ROOT.name=='aaowasi-projects' or (ROOT/'engine').exists()
data=json.loads((ROOT/'content/projects.json').read_text())
plans=json.loads((ROOT/'content/enterprise-plans.json').read_text())
seen=set()
def safe_url(value):
 if not value:return ''
 if value.startswith('/') and not value.startswith('//'):return value
 p=urlsplit(value)
 if p.scheme!='https' or not p.netloc:raise ValueError('Only relative paths or HTTPS destinations are allowed')
 return value
cards=[]
for p in data:
 if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',p['slug']):raise ValueError('Invalid slug')
 if p['slug'] in seen:raise ValueError('Duplicate slug')
 seen.add(p['slug'])
 # Content format is open; actions are capability-driven, not tied to a type enum.
 actions=[]
 for field,label in [('liveUrl','Open project'),('caseStudyUrl','Read case study'),('downloadUrl','Download artifact'),('codeUrl','View source')]:
  u=safe_url(p.get(field,''))
  if u:actions.append((u,label))
 if IS_PROJECT and p.get('sourcePath'):
  actions.insert(0,('/work/'+p['slug']+'/','Explore work'))
 elif p.get('liveUrl'):actions[0]=(p['liveUrl'],'Explore work')
 primary=actions[0][0] if actions else None
 title='<a href="'+e(primary,quote=True)+'">'+e(p['title'])+'</a>' if primary else e(p['title'])
 buttons=''.join('<a href="'+e(u,quote=True)+'">'+e(label)+' ↗</a>' for u,label in actions[:3])
 cards.append('<article class="card" data-project data-domain="'+e(p['domain'],quote=True)+'" data-type="'+e(p['type'],quote=True)+'"><div class="visual" aria-hidden="true"><span>'+e(p['id'])+'</span><small>'+e(p['domain'])+'<br>Evidence / decisions</small></div><span class="eyebrow">'+e(p['domain'])+' / '+e(p['type'])+'</span><h3>'+title+'</h3><p>'+e(p['summary'])+'</p><p class="chips">'+e(' · '.join(p.get('frameworks',[])[:3]))+'</p><div class="actions">'+buttons+'</div></article>')
 if IS_PROJECT and p.get('sourcePath'):
  manifest=json.loads((ROOT/p['sourcePath']).read_text())
  template=(ROOT/'templates/project.html').read_text()
  plan=plans[p['id']]
  plan_html=''.join('<section class="section case-plan"><span class="eyebrow">'+str(i+1).zfill(2)+'</span><div><h2>'+e(s['title'].split(' / ',1)[1])+'</h2><p>'+e(s['body'])+'</p></div></section>' for i,s in enumerate(plan['sections']))
  plan_html+='<section class="section content source-list"><h2>Primary sources</h2><ul>'+''.join('<li><a href="'+e(safe_url(s['url']),quote=True)+'">'+e(s['title'])+' ↗</a></li>' for s in plan['sources'])+'</ul><p>References checked 24 September 2026. Public framework concepts only; no reproduction of paid ISO control text. Taxonomy references are not observed client outcomes.</p><a href="/data/workspace-schema.json">Inspect the exact schema ↗</a></section>'
  values={'PLAN_SECTIONS':plan_html,'TIER':str(plan['tier']),'TITLE':e(p['title']),'ID':e(p['id']),'DOMAIN':e(p['domain']),'SUMMARY':e(p['summary']),'PURPOSE':e(p['outcome']),'BASIS':e(p.get('evidenceBasis','Work sample')),'CODE':e(safe_url(p.get('codeUrl',''))),'SLUG':p['slug'],'SOURCE':e(p['sourcePath']), 'CAPABILITIES':''.join('<li>'+e(x)+'</li>' for x in manifest['capabilities']),'OUTPUTS':''.join('<li>'+e(x)+'</li>' for x in manifest['outputs']),'GUARDRAILS':''.join('<li>'+e(x)+'</li>' for x in manifest['guardrails'])}
  for k,v in values.items():template=template.replace('{{'+k+'}}',v)
  target=ROOT/'site/work'/p['slug']/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(template)
text=(ROOT/'templates/gallery.html').read_text().replace('{{PROJECT_CARDS}}',''.join(cards))
for key,field in [('DOMAINS','domain'),('TYPES','type')]:text=text.replace('{{'+key+'}}',''.join('<option>'+e(x)+'</option>' for x in sorted({p[field] for p in data})))
text=text.replace('>10 projects</p>','>'+str(len(data))+' projects</p>')
(ROOT/('site/index.html' if IS_PROJECT else 'site/work/index.html')).write_text(text)
(ROOT/'site/data').mkdir(exist_ok=True)
shutil.copyfile(ROOT/'content/projects.json',ROOT/'site/data/projects.json')
# Refresh the hub's selected-work links and descriptions from the same catalogue.
if not IS_PROJECT:
 template=(ROOT/'templates/home.html').read_text()
 chosen=sorted([p for p in data if p.get('featured')],key=lambda p:p.get('featuredOrder',99))[:3]
 rows=[]
 for i,p in enumerate(chosen):
  u=next((safe_url(p.get(k,'')) for k in ['liveUrl','caseStudyUrl','downloadUrl','codeUrl'] if p.get(k)), '/work/')
  rows.append('<article class="work-row"><span class="eyebrow">0'+str(i+1)+'</span><div><p class="eyebrow">'+e(p['domain'])+'</p><h3><a href="'+e(u)+'">'+e(p['title'])+'</a></h3><span class="chips">'+e(p.get('evidenceBasis','Work sample'))+'</span></div><p class="muted">'+e(p['summary'])+'</p><a class="arrow" aria-label="Explore '+e(p['title'],quote=True)+'" href="'+e(u)+'">↗</a></article>')
 (ROOT/'site/index.html').write_text(template.replace('{{FEATURED_WORK}}',''.join(rows)))
print('Generated catalogue:',len(data),'projects')
