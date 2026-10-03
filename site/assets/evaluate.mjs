const $=id=>document.getElementById(id);let currentReport=null,requestId=null,requestBody=null;
const status=(text)=>{$('evaluation-status').textContent=text;};
try{
 const r=await fetch('/data/evaluation-domains.json');if(!r.ok)throw Error();const domains=await r.json();
 for(const domain of domains){const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.name='domain';input.value=domain;label.append(input,document.createTextNode(domain));$('evaluation-domains').append(label);}
 const available=await fetch('/api/status',{redirect:'error'});if(!available.ok)throw Error();const config=await available.json();
 if(!config.available)throw Error();$('organization-login').hidden=false;$('access-status').textContent='Sign in with provisioned organization access to run an evaluation.';
 $('processor-note').textContent='Processing provider: '+config.provider+'. Review the agreed data-handling terms before submitting.';
 const account=await fetch('/api/account',{redirect:'error'});if(account.ok){const a=await account.json();$('access-status').textContent=a.organization+': '+a.remaining+' evaluations remaining.';$('evaluation-panel').hidden=a.remaining===0;$('request-access').textContent=a.remaining===0?'Discuss continued access ↗':'Discuss implementation ↗';}
}catch{$('access-status').textContent='Request organization access to confirm scope, processing terms and your evaluation allowance.';}
$('evaluation-form').addEventListener('submit',async event=>{
 event.preventDefault();const f=new FormData(event.target);const domains=f.getAll('domain');if(f.get('customDomain')?.trim())domains.push(f.get('customDomain').trim());if(!domains.length){status('Choose at least one review area.');return;}
 const data={scope:f.get('scope'),context:f.get('context'),domains,authorized:f.has('authorized')};const body=JSON.stringify(data);if(body!==requestBody){requestId=crypto.randomUUID();requestBody=body;}
 const button=$('run-evaluation');button.disabled=true;status('Reviewing the decision and evidence gaps…');
 try{const response=await fetch('/api/evaluate',{method:'POST',redirect:'error',headers:{'Content-Type':'application/json','Idempotency-Key':requestId},body});const result=await response.json();if(!response.ok){if(response.status===402){$('request-access').textContent='Discuss continued access ↗';button.textContent='Organization allowance reached';}if(response.status!==409){requestId=null;requestBody=null;}throw Error(result.error||'Evaluation unavailable.');}
 currentReport=result;$('report-findings').replaceChildren();for(const f of result.findings){const article=document.createElement('article');article.className='resume-item';const heading=document.createElement('h3');heading.textContent=f.domain;article.append(heading);for(const [label,key]of [['Finding','finding'],['Evidence needed','evidenceNeeded'],['Next action','nextAction'],['Reviewer','owner']]){const p=document.createElement('p'),strong=document.createElement('strong');strong.textContent=label+': ';p.append(strong,document.createTextNode(f[key]));article.append(p);}$('report-findings').append(article);}
 $('evaluation-result').hidden=false;status('Review completed. Findings require accountable review against supporting evidence.');requestId=null;requestBody=null;
 }catch(e){status(e.message||'The evaluation could not complete. Your input is preserved.');}finally{button.disabled=button.textContent==='Organization allowance reached';}
});
$('download-report').addEventListener('click',()=>{if(!currentReport)return;const u=URL.createObjectURL(new Blob([JSON.stringify(currentReport,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=u;a.download='governance-decision-review.json';a.click();URL.revokeObjectURL(u);});
