import {evaluateScenario,scenarioMemo,SCENARIO_LIMIT} from './scenario-core.mjs';

const fixtures=[
 {id:'D14-1',url:'/samples/ai-governance/1.json'},
 {id:'D07-2',url:'/samples/audit-readiness/2.json'},
 {id:'D12-3',url:'/samples/processor-governance/3.json'}
];
const $=id=>document.getElementById(id);
const message=(str,failed=false)=>{$('outcome-status').textContent=str;$('outcome-status').classList.toggle('error',failed);};
const download=(content,filename,type)=>{
 const u=URL.createObjectURL(new Blob([content],{type}));
 const a=document.createElement('a');a.href=u;a.download=filename;a.click();
 setTimeout(()=>URL.revokeObjectURL(u),1000);
};
let configs,catalog,pack;
function show(p){
 pack=p;
 const counts=p.decisionLabMetrics,review=p.domainReview,controls=p.workspaceMetrics;
 const gate=counts.high>0?'HIGH RISK / HOLD':review.readiness.gate==='Ready for accountable review'&&review.readiness.percent===100&&controls.coverage===100?'READY / HUMAN REVIEW':'REVIEW / HOLD';
 $('outcome-title').textContent=p.scenarioId+' · '+review.title;
 $('outcome-gate').textContent=gate;
 $('outcome-gate').dataset.gate=gate.startsWith('READY')?'ready':'hold';
 $('outcome-readiness').textContent=review.readiness.percent+'%';
 $('outcome-coverage').textContent=controls.coverage.toFixed(0)+'%';
 $('outcome-high').textContent=String(counts.high);
 $('outcome-deadline').textContent=p.notification?.deadlineAt||'Not declared';
 $('outcome-basis').textContent='Snapshot '+review.reportingDate+' · synthetic input assertions. Valid HTTPS-shaped references are not fetched, authenticated, or content-verified. '+(p.notification?.applicability||'No reporting clock in this case.');
 const list=$('outcome-actions');
 list.replaceChildren();
 const issues=p.workspace.records.filter(r=>r.type==='issue'&&r.status!=='Closed');
 const items=[...issues.map(r=>({heading:r.title+' — '+(r.owner||review.reviewer),detail:r.correctiveAction||'Review required'})),...review.findings.map(f=>({heading:f.priority+' · '+f.finding,detail:f.nextAction}))];
 if(!items.length)items.push({heading:'No recorded evidence gaps in this synthetic fixture',detail:'Request independent evidence verification, reporting-period scope and authorized sign-off before any external assurance claim.'});
 for(const x of items.slice(0,9)){
  const li=document.createElement('li'),strong=document.createElement('strong'),detail=document.createElement('span');
  strong.textContent=x.heading;detail.textContent=' — '+x.detail;li.append(strong,detail);list.append(li);
 }
 $('outcome-json').textContent=JSON.stringify(p,null,2);
 $('outcome-export-json').disabled=false;$('outcome-export-memo').disabled=false;
 message('Recalculated '+p.scenarioId+': '+counts.total+' supplier/service records; '+review.readiness.confirmed+'/'+review.readiness.total+' recorded domain checks. This is not a legal or certification opinion.');
}
async function init(){
 const [cr,ca]=await Promise.all([fetch('/data/domain-reviews.json'),fetch('/data/suite-catalog.json')]);
 if(!cr.ok||!ca.ok)throw Error('Canonical evaluation catalogs unavailable.');
 [configs,catalog]=await Promise.all([cr.json(),ca.json()]);
 await select(fixtures[0].url);
}
async function select(url){
 try{
  message('Validating synthetic scenario...');
  const response=await fetch(url);
  if(!response.ok)throw Error('Sample could not be downloaded.');
  const raw=await response.text();
  if(new TextEncoder().encode(raw).length>SCENARIO_LIMIT)throw Error('Scenario is too large.');
  show(evaluateScenario(JSON.parse(raw),configs,catalog));
 }catch(e){message('Scenario rejected: '+e.message,true);}
}
document.querySelectorAll('[data-outcome-select]').forEach(button=>button.addEventListener('click',()=>{
 const scenario=fixtures.find(x=>x.id===button.dataset.outcomeSelect);
 if(scenario)select(scenario.url);
 $('outcome-console').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'});
}));
$('outcome-upload').addEventListener('change',async event=>{
 try{
  const file=event.target.files?.[0];
  if(!file)return;
  if(file.size>SCENARIO_LIMIT)throw Error('Maximum 16 KB for scenario files.');
  const raw=JSON.parse(await file.text());
  show(evaluateScenario(raw,configs,catalog));
 }catch(e){message('Import rejected; previous result preserved: '+e.message,true);}
 finally{event.target.value='';}
});
$('outcome-export-json').onclick=()=>pack&&download(JSON.stringify(pack,null,2),pack.scenarioId+'-decision-pack-v2.json','application/json');
$('outcome-export-memo').onclick=()=>pack&&download(scenarioMemo(pack),pack.scenarioId+'-decision-memo.md','text/markdown;charset=utf-8');
init().catch(e=>message('Unable to start the demonstration: '+e.message,true));
