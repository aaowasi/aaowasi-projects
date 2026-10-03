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
  function=ROOT.parent/'functions'/(unquote(u.path).lstrip('/')+'.js')
  if not path.exists() and not function.exists():errors.append(str(p)+': missing '+link)
 for token in ['{{PROJECT','{{TITLE','{{FEATURED']:
  if token in p.read_text():errors.append(str(p)+': unresolved template')
assert not errors,'\n'.join(errors)
for p in ROOT.rglob('*.json'):json.loads(p.read_text())
print('PASS:',count,'HTML pages, local destinations, unique IDs and JSON')

# Metadata and sitemap integrity are part of the static delivery contract.
from xml.etree import ElementTree as ET
listed={x.text for x in ET.parse(ROOT/'sitemap.xml').iter() if x.tag.endswith('}loc')}
for page in ROOT.rglob('*.html'):
 class Meta(HTMLParser):
  def __init__(self):super().__init__();self.canonical=[];self.meta={}
  def handle_starttag(self,tag,attrs):
   a=dict(attrs)
   if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
   if tag=='meta':self.meta[a.get('property',a.get('name'))]=a.get('content')
 m=Meta();m.feed(page.read_text())
 assert len(m.canonical)==1, str(page)+': canonical count'
 assert m.meta.get('description') and m.meta.get('og:image'), str(page)+': missing SEO metadata'
 image=ROOT/urlsplit(m.meta['og:image']).path.lstrip('/')
 assert image.exists(), str(page)+': missing social image'
 if page.name!='404.html':assert m.canonical[0] in listed,str(page)+': missing sitemap route'
 assert m.meta.get('og:url')==m.canonical[0]
print('PASS: canonical metadata, social assets and sitemap routes')

import re, hashlib, base64
headers=(ROOT/'_headers').read_text()
assert "script-src 'self'" in headers and "'unsafe-inline'" not in headers
for page in ROOT.rglob('*.html'):
 for payload in re.findall(r'<script type="application/ld\+json" data-seo>(.*?)</script>',page.read_text(),re.S):
  data=json.loads(payload)
  assert data.get('@context')=='https://schema.org' and data.get('@graph')
  digest=base64.b64encode(hashlib.sha256(payload.encode()).digest()).decode()
  assert "'sha256-"+digest+"'" in headers, str(page)+': JSON-LD CSP hash missing'
print('PASS: structured data parses and exact CSP hashes match')
