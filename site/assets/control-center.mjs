import {evaluateScenario,scenarioMemo,SCENARIO_LIMIT} from './scenario-core.mjs';
import {validate as validateSuite} from './suite-core.mjs';
import {renderExecutiveDashboard,executiveMemo} from './dashboard-ui.mjs';
import {projectScenarioRisks} from './dashboard-core.mjs';
const $=id=>document.getElementById(id);
const download=(content,filename,type='application/json')=>{const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=filename;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
const examples=[
 {id:'D14-1',name:'AI vendor onboarding · HIGH / HOLD',url:'/samples/ai-governance/1.json'},
 {id:'D07-2',name:'Cloud audit readiness · 100% recorded checks',url:'/samples/audit-readiness/2.json'},
 {id:'D12-3',name:'Cross-border shadow AI · HIGH / HOLD',url:'/samples/processor-governance/3.json'}
];
let config,catalog,pack,state={version:1,records:[],updatedAt:null},asOf=new Date().toISOString().slice(0,10),ready=false;
const status=(value,error=false)=>{$('cc-status').textContent=value;$('cc-status').dataset.error=String(error);};
function snapshot(){
 const perspective=$('cc-domain').value,appetite=Number($('cc-appetite').value);
 const result=renderExecutiveDashboard($('cc-dashboard'),state.records,asOf,{domain:perspective,appetite,projectedRisk:projectScenarioRisks(pack)});
 return result;
}
let lastSummary=null;
function redraw(){lastSummary=snapshot();$('cc-snapshot').value=asOf;$('cc-count').textContent=state.records.length+' linked typed records in active browser session · '+(pack?pack.scenarioId:'imported organization data');}
function evaluate(raw){
 if(raw?.scenarioVersion===1){
  const p=evaluateScenario(raw,config,catalog);
  pack=p;state=p.workspace;asOf=p.domainReview.reportingDate;
  $('cc-domain').value='';
  $('cc-gate').textContent=p.scenarioId+' · '+p.domainReview.readiness.gate+' · '+p.decisionLabMetrics.high+' high-priority supplier signals · Version-2 decision export ready.';
  return 'Scenario '+p.scenarioId+' validated. All dashboard components recalculated in the browser.';
 }
 if(raw?.version===1){
  const verified=validateSuite(raw,catalog);
  pack=null;state=verified;
  $('cc-domain').value='';
  $('cc-gate').textContent='Typed 29-domain suite imported. No decision pack from a scenario; the executive memo remains exportable.';
  return 'Typed suite dataset imported; all 29 perspectives can be inspected.';
 }
 throw Error('Use a version 1 typed suite JSON or a synthetic scenarioVersion 1 JSON. Version-2 decision exports are reports, not import files.');
}
async function select(url){
 try{
  status('Loading and validating demonstration…');
  const r=await fetch(url);if(!r.ok)throw Error('Sample not available on this site.');
  const text=await r.text();if(new TextEncoder().encode(text).length>SCENARIO_LIMIT)throw Error('Demo exceeds scenario limit.');
  status(evaluate(JSON.parse(text)));redraw();
 }catch(e){status('Unable to load sample: '+e.message,true);}
}
async function initialize(){
 const [a,b]=await Promise.all([fetch('/data/domain-reviews.json'),fetch('/data/suite-catalog.json')]);
 if(!a.ok||!b.ok)throw Error('Could not load the governance catalogs.');
 [config,catalog]=await Promise.all([a.json(),b.json()]);ready=true;
 for(const d of catalog.domains){const option=document.createElement('option');option.value=d.slug;option.textContent=d.title||d.name||d.slug.replaceAll('-',' ');$('cc-domain').append(option);}
 for(const demo of examples){const option=document.createElement('option');option.value=demo.url;option.textContent=demo.id+' · '+demo.name;$('cc-demo').append(option);}
 await select(examples[0].url);
}
$('cc-demo').onchange=()=>select($('cc-demo').value);
$('cc-load').onclick=()=>select($('cc-demo').value);
$('cc-domain').onchange=()=>{try{redraw();status('Domain perspective updated. Shared evidence references remain connected.');}catch(e){status(e.message,true);}};
$('cc-appetite').oninput=()=>{try{redraw();status('Illustrative risk threshold updated; organization approval is not implied.');}catch(e){status(e.message,true);}};
$('cc-snapshot').onchange=()=>{try{const previous=asOf;asOf=$('cc-snapshot').value;redraw();status('Snapshot date changed; evidence freshness recalculated.');}catch(e){status('Invalid reporting date: '+e.message,true);}};
$('cc-import').onchange=async e=>{
 const input=e.currentTarget;
 try{
  const file=input.files?.[0];if(!file)return;
  if(!ready)throw Error('Reference catalogs are loading.');
  if(!file.name.toLowerCase().endsWith('.json'))throw Error('This control accepts a JSON scenario or suite export. CSV can be imported in Decision Lab.');
  if(file.size>20*1024*1024)throw Error('Maximum typed suite file size 20 MB.');
  const raw=JSON.parse(await file.text());
  status(evaluate(raw));redraw();
  $('cc-status').scrollIntoView({block:'nearest'});
 }catch(err){status('Import rejected, previous state preserved: '+err.message,true);}
 finally{input.value='';}
};
$('cc-export-suite').onclick=()=>download(JSON.stringify(state,null,2),'grc-suite-29-domains.json');
$('cc-export-pack').onclick=()=>pack?download(JSON.stringify(pack,null,2),pack.scenarioId+'-decision-pack-v2.json'):status('First load a scenario fixture to export a version-2 decision pack.',true);
$('cc-export-memo').onclick=()=>{try{const summary=snapshot();let memo=executiveMemo(summary);if(pack)memo+='\n\n'+scenarioMemo(pack);download(memo,'grc-executive-decision-brief.md','text/markdown;charset=utf-8');status('Executive decision memo prepared for download.');}catch(e){status(e.message,true);}};
$('cc-export-csv').onclick=()=>{
 try{
  const rows=(lastSummary||snapshot()).riskRows;
  const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
  const lines=[['id','title','owner','domain','inherent','residual','riskBand','aboveAppetite'],...rows.map(r=>[r.id,r.title,r.owner,r.domain,r.inherent??'',r.residual??'',r.residualBand,r.aboveAppetite===null?'Not assessed':String(r.aboveAppetite)])];
  const csv=lines.map(r=>r.map(v=>{const text=String(v??'');return quote(/^[=+@\-\t\r]/.test(text)?'\''+text:text);}).join(',')).join('\r\n');
  download(csv,'grc-risk-register.csv','text/csv;charset=utf-8');
 }catch(e){status(e.message,true);}
};
initialize().catch(e=>status('Control Center unavailable: '+e.message,true));
