"""Consolidate project details and preserve former section URLs as redirects."""
from html import escape, unescape
import json, re, shutil

def split_projects(root):
 redirects_path=root/'content/legacy-section-redirects.json'
 redirects=json.loads(redirects_path.read_text()) if redirects_path.exists() else {}
 for page in sorted((root/'site/work').glob('*/index.html')):
  source=page.read_text();main=re.search(r'<main\b[^>]*>(.*?)</main>',source,re.S)
  if not main:continue
  body=main.group(1);sections=[];start=None;depth=0
  for token in re.finditer(r'</?section\b[^>]*>',body):
   if token.group().startswith('</'):
    depth-=1
    if depth==0 and start is not None:sections.append(body[start:token.end()])
   else:
    if depth==0:start=token.start()
    depth+=1
  if len(sections)<2:continue
  routes=[]
  for i,section in enumerate(sections[1:],1):
   heading=re.search(r'<h2[^>]*>(.*?)</h2>',section,re.S)
   title=unescape(re.sub('<[^>]+>',' ',heading.group(1))).strip() if heading else 'Decision details'
   slug=re.sub('[^a-z0-9]+','-',title.lower()).strip('-') or f'details-{i}'
   if any(x[0]==slug for x in routes):slug+=f'-{i}'
   routes.append((slug,title,section,heading))
  prefix='/work/'+page.parent.name+'/'
  nav='<nav class="project-index" aria-label="Project contents">'+''.join('<a href="#'+slug+'">'+escape(title)+'</a>' for slug,title,_,_ in routes)+'</nav>'
  details=[]
  for slug,title,section,heading in routes:
   inside=re.sub(r'^<section\b[^>]*>|</section>$','',section)
   if heading:inside=inside.replace(heading.group(0),'',1)
   inside=re.sub(r'<span class="eyebrow">\d+</span>','',inside)
   details.append('<details '+('open ' if not details else '')+'class="project-detail" id="'+slug+'"><summary>'+escape(title)+'</summary><div>'+inside+'</div></details>')
  page.write_text(source[:main.start(1)]+sections[0]+nav+''.join(details)+source[main.end(1):])
  for child in page.parent.iterdir():
   if child.is_dir() and (child/'index.html').exists():
    target=prefix+'#'+child.name
    redirects[prefix+child.name+'/']=target
    shutil.rmtree(child)
 for route,target in list(redirects.items()):
  base,_,fragment=target.partition('#');page=root/'site'/base.strip('/')/'index.html'
  if not page.exists():base='/work/governance-program/';fragment=''
  elif fragment and not re.search(r'id=[\"\']'+re.escape(fragment)+r'[\"\']',page.read_text()):fragment=''
  redirects[route]=base+('#'+fragment if fragment else '')
 redirects_path.write_text(json.dumps(redirects,indent=2)+'\n')
 (root/'site/_redirects').write_text('\n'.join(path+' '+target+' 301' for path,target in sorted(redirects.items()))+'\n')
