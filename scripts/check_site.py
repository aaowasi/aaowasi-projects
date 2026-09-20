from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1]/'site'
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='h1':self.h1+=1
  if 'id' in d:self.ids.append(d['id'])
  for attr in ['href','src']:
   if attr in d:self.links.append(d[attr])
errors=[];count=0
for p in ROOT.rglob('*.html'):
 a=Audit();a.feed(p.read_text());count+=1
 if a.h1!=1:errors.append(str(p)+': expected one h1')
 if len(a.ids)!=len(set(a.ids)):errors.append(str(p)+': duplicate IDs')
 for link in a.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  path=ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else p.parent/unquote(u.path)
  if not u.path:continue
  if path.is_dir():path=path/'index.html'
  if not path.exists():errors.append(str(p)+': missing '+link)
 for token in ['{{PROJECT','{{TITLE','{{FEATURED']:
  if token in p.read_text():errors.append(str(p)+': unresolved template')
assert not errors,'\n'.join(errors)
for p in ROOT.rglob('*.json'):json.loads(p.read_text())
print('PASS:',count,'HTML pages, local destinations, unique IDs and JSON')
