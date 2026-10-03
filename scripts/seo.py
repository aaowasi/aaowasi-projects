"""Deterministic metadata/sitemap generation for public static routes."""
import base64
import hashlib
import json
import re
from html import escape, unescape
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

def apply_seo(root):
    project=(root/'engine').exists()
    origin='https://aaowasi-projects.pages.dev' if project else 'https://aaowasi.pages.dev'
    descriptions={
        '/':'Connected AI governance, third-party AI risk, technology risk and assurance workflows by Abdullah Al Owasi. Inspect live mechanics, evidence boundaries and decision outputs.' if project else 'Evidence-led AI governance, supplier risk and assurance delivery by Abdullah Al Owasi. Inspect the work and scope a governance review.',
        '/profile/':'Abdullah Al Owasi: governance strategy and delivery, AI risk, supplier assurance and control evidence. Read the executive bio, competencies and resume.',
        '/services/':'Scope an AI governance sprint, supplier and assurance sprint or recurring governance review with defined evidence, responsibilities and decision outputs.',
        '/contact/':'Prepare a bounded AI, supplier-risk or assurance review brief: decision needed, available evidence, target date and agreed outputs.',
        '/results/':'Recorded GitHub Actions observations with exact commits, timestamps and source runs for the AAO governance portfolio. Inspect what the checks prove and what they do not.',
        '/workspace/':'Change AI, supplier, privacy and evidence metadata across connected governance modules; inspect risk priorities, reviewer gates and decision exports.',
        '/work/':'Explore connected AI governance, third-party risk, technology-risk and assurance projects with implementation mechanics, primary sources and human review boundaries.'
    }
    urls=[]
    script_hashes=set()
    for page in sorted((root/'site').rglob('*.html')):
        relative=page.relative_to(root/'site').as_posix()
        route='/' if relative=='index.html' else '/'+relative.removesuffix('index.html') if relative.endswith('/index.html') else '/'+relative
        url=origin+route
        s=page.read_text()
        title=unescape(re.search(r'<title>(.*?)</title>',s,re.S).group(1))
        description=descriptions.get(route, title.split(' | ')[0]+': implementation scope, decision mechanics and review boundaries in Abdullah Al Owasi’s governance portfolio.')
        # Replace only metadata owned by this generator; preserve other page tags.
        s=re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>','',s,flags=re.I)
        s=re.sub(r'<meta\b[^>]*(?:name|property)=["\'](?:description|robots|og:[^"\']+|twitter:[^"\']+)["\'][^>]*>','',s,flags=re.I)
        s=re.sub(r'<script type="application/ld\+json" data-seo>.*?</script>','',s,flags=re.S)
        image=origin+'/assets/aao_white.webp'
        tags='<link rel="canonical" href="'+url+'"><meta name="description" content="'+escape(description,quote=True)+'">'
        for key,value in {'og:title':title,'og:description':description,'og:type':'website','og:url':url,'og:image':image,'og:image:alt':'Abdullah Al Owasi brand artwork'}.items():tags+='<meta property="'+key+'" content="'+escape(value,quote=True)+'">'
        for key,value in {'twitter:card':'summary_large_image','twitter:title':title,'twitter:description':description,'twitter:image':image}.items():tags+='<meta name="'+key+'" content="'+escape(value,quote=True)+'">'
        if relative=='404.html':tags+='<meta name="robots" content="noindex,follow">'
        else:urls.append(url)
        if route in ['/','/profile/']:
            graph=[{'@type':'WebSite','@id':origin+'/#website','url':origin+'/','name':'AAO Governance Portfolio' if project else 'Abdullah Al Owasi'}]
            if not project:graph.append({'@type':'Person','@id':origin+'/#person','name':'Abdullah Al Owasi','url':origin+'/profile/','sameAs':['https://github.com/aaowasi','https://www.linkedin.com/in/aaowasi/'],'knowsAbout':['AI governance','Supplier risk','Control assurance']})
            data=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
            script_hashes.add("'sha256-"+base64.b64encode(hashlib.sha256(data.encode()).digest()).decode()+"'")
            tags+='<script type="application/ld+json" data-seo>'+data+'</script>'
        page.write_text(s.replace('</head>',tags+'</head>'))
    tree=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for url in urls:SubElement(SubElement(tree,'url'),'loc').text=url
    ElementTree(tree).write(root/'site/sitemap.xml',encoding='utf-8',xml_declaration=True)
    (root/'site/robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+origin+'/sitemap.xml\n')

    headers=root/'site/_headers'
    if headers.exists():
        text=headers.read_text()
        text=re.sub(r"script-src 'self'[^;]*", "script-src 'self' "+' '.join(sorted(script_hashes)), text)
        headers.write_text(text)
