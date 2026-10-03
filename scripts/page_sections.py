"""Publish each project section as a focused route with local navigation."""
from pathlib import Path
from html import escape, unescape
import re

def split_projects(root):
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
   routes.append((slug,title,section))
  prefix='/work/'+page.parent.name+'/'
  directory='<nav class="section-directory" aria-label="Project sections">'+''.join('<a href="'+prefix+slug+'/">'+escape(title)+' →</a>' for slug,title,_ in routes)+'</nav>'
  overview=sections[0].replace('</section>',directory+'</section>')
  page.write_text(source[:main.start(1)]+overview+source[main.end(1):])
  for slug,title,section in routes:
   # Existing section becomes this page's single main section; keep other headings below the page title.
   section=re.sub(r'<h2([^>]*)>(.*?)</h2>',r'<h1\1>\2</h1>',section,count=1,flags=re.S)
   section=section.replace('</section>','<nav class="section-directory" aria-label="Project navigation"><a href="'+prefix+'">Project overview →</a></nav></section>')
   if '<h1' not in section:section=section.replace('>','><h1>'+escape(title)+'</h1>',1)
   text=source[:main.start(1)]+section+source[main.end(1):]
   text=re.sub(r'<title>.*?</title>','<title>'+escape(title)+' | '+escape(page.parent.name.replace('-',' ').title())+'</title>',text)
   target=page.parent/slug/'index.html';target.parent.mkdir(exist_ok=True);target.write_text(text)
