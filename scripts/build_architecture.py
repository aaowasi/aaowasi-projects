from html import escape as e
import json

def render_architecture(root):
    data=json.loads((root/'content/domain-matrix.json').read_text())
    page=(root/'templates/architecture.html').read_text()
    for group in ['enterprise','technical']:
        rows=[]
        for item in data:
            if item['group']!=group:continue
            destination=item['workflow']
            if not destination.startswith('/work/') or not (root/'site'/destination.strip('/')/'index.html').exists():
                raise ValueError('Matrix workflow must resolve to an inspectable project')
            rows.append('<tr><th scope="row">'+e(item['domain'])+'</th><td>'+e(item['framework'])+'</td><td><a href="'+e(destination,quote=True)+'">'+e(item['output'])+' →</a></td></tr>')
        page=page.replace('{{'+group.upper()+'_ROWS}}',''.join(rows)).replace('{{'+group.upper()+'_COUNT}}',str(len(rows)))
    return page
