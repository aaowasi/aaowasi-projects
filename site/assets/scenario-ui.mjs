import {evaluateScenario,scenarioMemo,SCENARIO_LIMIT} from './scenario-core.mjs';
const download=(value,name,type)=>{const url=URL.createObjectURL(new Blob([value],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
const host=document.querySelector('[data-review-inspector]')||document.querySelector('main');
if(host){
 if(!document.querySelector('link[href="/assets/scenario-ui.css"]')){const l=document.createElement('link');l.rel='stylesheet';l.href='/assets/scenario-ui.css';document.head.append(l);}
 const panel=document.createElement('section');panel.className='review-inspector scenario-walkthrough';panel.id='scenario-walkthrough';
 panel.innerHTML=`<p class="eyebrow">EXECUTABLE CLIENT DEMONSTRATION · ALL IN YOUR BROWSER</p><h2>Download. Import. Inspect. Export.</h2>
 <p>Choose a synthetic example, or select its JSON file. The validated scenario runs immediately in this browser, updates the active review/register and produces a decision pack. No desktop software or upload is required.</p>
 <div class="scenario-import-grid"><label>Scenario<select data-scenario-choice></select></label><a class="button" data-scenario-download download>Download sample JSON ↓</a><label class="scenario-file-label">Import a scenario JSON<input data-scenario-import type="file" accept=".json,application/json"></label></div>
 <p class="scenario-inline-note">Importing an example replaces only the current browser session's active dataset. Export any earlier edits first. No server data is changed.</p>
 <p class="scenario-status" data-scenario-status role="status" aria-live="polite">Preparing 29-domain scenario definitions…</p>
 <div class="scenario-result" data-scenario-result hidden><div class="scenario-cards"><div><span>Decision gate</span><strong data-scenario-gate>—</strong></div><div><span>Domain readiness</span><strong data-scenario-readiness>—</strong></div><div><span>Tested control coverage</span><strong data-scenario-coverage>—</strong></div><div><span>High risk signals</span><strong data-scenario-high>—</strong></div></div>
 <div class="scenario-summary"><h3 data-scenario-title>Decision preview</h3><p data-scenario-reason></p><h4>Accountable actions &amp; evidence gaps</h4><ul data-scenario-actions></ul></div></div>
 <div class="actions scenario-export"><button type="button" data-scenario-pack disabled>Export Decision Pack v2 ↓</button><button type="button" data-scenario-memo disabled>Export decision memo ↓</button><a href="/control-center/">Executive control center →</a><a href="/samples/">All 87 domain cases →</a></div>
 <details data-scenario-details><summary>Full calculation, schema and decision JSON</summary><pre class="review-json" data-scenario-output></pre></details>
 <p class="small">All input fixtures are synthetic. HTTPS-shaped evidence links are not fetched or independently verified. A 100% recorded score is not certification; legal applicability and approvals remain with a named reviewer.</p>`;
 if(host.tagName==='MAIN')host.prepend(panel);else host.before(panel);
 let configs,catalog,index,pack;
 const $=selector=>panel.querySelector(selector);
 const status=$('[data-scenario-status]'),choice=$('[data-scenario-choice]'),link=$('[data-scenario-download]');
 function announce(text,error=false){status.textContent=text;status.dataset.kind=error?'error':'success';}
 function display(next){
  pack=next;
  const r=next.domainReview,m=next.workspaceMetrics,d=next.decisionLabMetrics;
  const gate=d.high>0?'HIGH / HOLD':r.readiness.percent===100&&m.coverage===100?'READY / HUMAN SIGN-OFF':'REVIEW / HOLD';
  $('[data-scenario-result]').hidden=false;
  $('[data-scenario-gate]').textContent=gate;
  $('[data-scenario-readiness]').textContent=r.readiness.percent+'%';
  $('[data-scenario-coverage]').textContent=m.coverage===null?'N/A':m.coverage+'%';
  $('[data-scenario-high]').textContent=String(d.high);
  $('[data-scenario-title]').textContent=next.scenarioId+' · '+r.title;
  $('[data-scenario-reason]').textContent=r.readiness.gate+' · Reporting snapshot: '+r.reportingDate+(next.notification?' · Conditional deadline: '+next.notification.deadlineAt:'');
  const items=$('[data-scenario-actions]');items.replaceChildren();
  const issues=next.workspace.records.filter(x=>x.type==='issue'&&x.status!=='Closed');
  for(const i of issues.slice(0,5)){const li=document.createElement('li');li.textContent=i.title+' — '+(i.owner||'Owner needed')+': '+(i.correctiveAction||'Review required');items.append(li);}
  for(const f of r.findings.slice(0,5)){const li=document.createElement('li');li.textContent=f.finding+' — '+f.nextAction;items.append(li);}
  if(!items.children.length){const li=document.createElement('li');li.textContent='No recorded gaps in this synthetic sample. Verify source evidence and obtain human approval.';items.append(li);}
  $('[data-scenario-output]').textContent=JSON.stringify(next,null,2);
  $('[data-scenario-pack]').disabled=false;$('[data-scenario-memo]').disabled=false;
  announce('✓ Scenario loaded successfully. '+next.scenarioId+' recalculated in this browser; the active review and register now reflect its records.');
 }
 // Re-render after a separate native import (suite, workspace or Decision Lab).
 document.addEventListener('scenario-evaluated',e=>{if(e.detail?.schemaVersion===2)display(e.detail);});
 function applyScenario(value){
  if(!configs||!catalog)throw Error('Scenario definitions are still loading. Try again in a moment.');
  const next=evaluateScenario(value,configs,catalog);
  const fixed=document.querySelector('[data-review-inspector]')?.dataset.reviewDomain;
  if(fixed&&fixed!==next.domain)throw Error('This is the '+next.domain+' scenario. Open its domain project or use the Control Center to review any domain.');
  // The user deliberately selected a synthetic JSON. This operation does not modify saved data.
  document.dispatchEvent(new CustomEvent('scenario-apply',{detail:next}));
  display(next);
  return next;
 }
 choice.onchange=()=>{link.href=choice.value;announce('Selected '+choice.selectedOptions[0]?.textContent+'. Download this JSON, then select it under Import.');};
 $('[data-scenario-import]').onchange=async e=>{
  const input=e.currentTarget;
  try{
   const f=input.files?.[0];if(!f)return;
   announce('Validating '+f.name+' in your browser…');
   if(f.size>SCENARIO_LIMIT)throw Error('The file exceeds 16 KB. Use a version 1 scenario JSON fixture.');
   if(!f.name.toLowerCase().endsWith('.json'))throw Error('Choose a JSON file.');
   const raw=JSON.parse(await f.text());
   applyScenario(raw);
   status.scrollIntoView({behavior:'instant',block:'nearest'});
  }catch(err){announce('Could not load this scenario. Previous review preserved. '+err.message,true);}
  finally{input.value='';}
 };
 $('[data-scenario-pack]').onclick=()=>pack&&download(JSON.stringify(pack,null,2),pack.scenarioId+'-decision-pack-v2.json','application/json');
 $('[data-scenario-memo]').onclick=()=>pack&&download(scenarioMemo(pack),pack.scenarioId+'-decision-memo.md','text/markdown;charset=utf-8');
 try{
  const results=await Promise.all(['/data/domain-reviews.json','/data/suite-catalog.json','/data/scenarios.json'].map(async url=>{const r=await fetch(url);if(!r.ok)throw Error('Scenario catalog unavailable: '+url);return r.json();}));
  [configs,catalog,index]=results;
  const options=()=>{
   const slug=document.querySelector('[data-review-inspector]')?.dataset.reviewDomain||document.querySelector('#domain-perspective')?.value||'';
   choice.replaceChildren();
   for(const item of index.filter(x=>!slug||x.domain===slug)){const o=document.createElement('option');o.value=item.url;o.textContent=item.id+' · '+item.title;choice.append(o);}
   link.href=choice.value||'/samples/';
  };
  options();
  document.querySelector('#domain-perspective')?.addEventListener('change',options);
  announce(index.length+' validated synthetic scenarios available. Choose a JSON file to populate the active review instantly.');
 }catch(err){announce('Unable to load scenario definitions: '+err.message,true);}
}
