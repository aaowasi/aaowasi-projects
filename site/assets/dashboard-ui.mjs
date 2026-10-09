import {executiveMetrics,executiveMemo} from './dashboard-core.mjs';

const element=(tag,content,className)=>{
 const el=document.createElement(tag);if(content!==undefined)el.textContent=String(content);if(className)el.className=className;return el;
};
const number=x=>x===null||x===undefined?'Not assessed':String(x);
export {executiveMemo};

/**
 * This component can be mounted in the Suite, the standalone control center,
 * or a domain. A filtered perspective keeps cross-domain evidence links alive.
 */
export function renderExecutiveDashboard(host,records,asOf,options={}){
 const summary=executiveMetrics(records,asOf,options);
 let selection=host.dataset.heatSelection||'';
 host.replaceChildren();
 const header=element('div',undefined,'cc-heading'),intro=element('div');
 intro.append(element('p','EXECUTIVE GOVERNANCE · '+summary.domain+' · '+summary.asOf,'eyebrow'),element('h2','Decisions before dashboards.'));
 intro.append(element('p','Synthetic or user-supplied browser-session records. No automated risk acceptance, certification, remote telemetry or legal opinion.','cc-muted'));
 header.append(intro);host.append(header);
 const grid=element('div',undefined,'cc-kpi-grid');
 const kpis=[
  ['Top exposure',summary.highResidual+' high residual','≥16 of 25; missing residual: '+summary.unassessedResidual],
  ['Risk appetite',summary.appetiteStatus,'Declared illustrative threshold: ≥'+summary.appetite],
  ['Control effectiveness',summary.controlCoverage===null?'N/A':summary.controlCoverage+'%',summary.controlPass+'/'+summary.controlTotal+' recorded current passes'],
  ['Incidents & losses',summary.openIncidents+' flagged', 'Incident-classified issues; financial losses not inferred'],
  ['Overdue actions',summary.overdue+' overdue',summary.openIssues+' open remediation issues'],
  ['Evidence freshness',summary.evidenceAges.older90+' aged >90d',summary.evidenceAges.older180+' aged >180 days']
 ];
 for(const [title,value,description]of kpis){
  const card=element('article',undefined,'cc-kpi');card.append(element('span',title),element('strong',value),element('small',description));grid.append(card);
 }
 host.append(grid);
 const sections=element('div',undefined,'cc-analysis-grid');
 const heatCard=element('section',undefined,'cc-card');
 heatCard.append(element('h3','Risk matrix · inherent 5 × 5'),element('p','Select a cell to inspect linked risk records. Vertical: likelihood 5 → 1. Horizontal: impact 1 → 5.','cc-muted'));
 const heat=element('div',undefined,'cc-risk-heat');heat.setAttribute('role','group');heat.setAttribute('aria-label','Interactive inherent risk matrix');
 const riskList=element('div',undefined,'cc-risk-list');riskList.setAttribute('aria-live','polite');
 const renderRiskList=()=>{
  riskList.replaceChildren();
  const matching=selection?summary.riskRows.filter(r=>r.likelihood+'-'+r.impact===selection):summary.topRisks;
  riskList.append(element('h4',selection?'Selected cell risks ('+matching.length+')':'Priority risk register ('+summary.risks+')'));
  for(const r of matching.slice(0,12)){
   const row=element('div',undefined,'cc-risk-item');
   row.append(element('strong',r.title||r.id),element('span','Inherent '+number(r.inherent)+' · Residual '+number(r.residual)+' · '+r.owner));
   riskList.append(row);
  }
  if(!matching.length)riskList.append(element('p','No risk records in this selection.','cc-muted'));
 };
 for(const c of summary.heat){
  const key=c.likelihood+'-'+c.impact,button=element('button',c.count,'cc-heat '+('cc-'+c.band.toLowerCase()));button.type='button';button.setAttribute('aria-label','Likelihood '+c.likelihood+', impact '+c.impact+', score '+c.score+': '+c.count+' risks; filter');button.setAttribute('aria-pressed',String(selection===key));button.title='L '+c.likelihood+' × I '+c.impact+' = '+c.score+' ('+c.band+')';
  button.onclick=()=>{selection=selection===key?'':key;host.dataset.heatSelection=selection;for(const b of heat.children)b.setAttribute('aria-pressed',String(b===button&&!!selection));renderRiskList();};
  heat.append(button);
 }
 heatCard.append(heat,riskList);
 const right=element('section',undefined,'cc-card');right.append(element('h3','Controls, remediation & regulatory hotspots'));
 const controlBars=element('div',undefined,'cc-bars');
 for(const [name,n,den] of [['Passing evidence',summary.controlPass,summary.controlTotal],['Unverified / failing controls',summary.controlTotal-summary.controlPass,summary.controlTotal]]){
  const wrap=element('div'),label=element('div',name+' · '+n+'/'+den,'cc-bar-label'),track=element('div',undefined,'cc-bar-track'),bar=element('span');bar.style.width=(den?Math.round(n/den*100):0)+'%';track.append(bar);wrap.append(label,track);controlBars.append(wrap);
 }
 right.append(controlBars);
 const queue=element('div',undefined,'cc-queue');queue.append(element('h4','Owner action queue'));
 for(const x of summary.issues.slice(0,5)){
  const row=element('div',undefined,'cc-action');
  row.append(element('strong',x.severity+' · '+x.title),element('span',x.owner+' — '+x.action));queue.append(row);
 }
 if(!summary.issues.length)queue.append(element('p','No open issues recorded in this dataset.','cc-muted'));
 right.append(queue);
 const frame=element('div',undefined,'cc-framework');frame.append(element('h4','Framework-linked evidence · not certification'));
 for(const f of summary.frameworks.slice(0,12)){
  const row=element('div',undefined,'cc-frame-row');
  row.append(element('strong',f.name),element('span',f.tested+'/'+f.obligations+' mapped and recorded tested'));
  frame.append(row);
 }
 if(!summary.frameworks.length)frame.append(element('p','No framework obligations in the selected records.','cc-muted'));
 right.append(frame);
 sections.append(heatCard,right);host.append(sections);
 const footer=element('p','Interpretation: High ≥16, Moderate ≥9 (likelihood × impact). Residual risk requires separately recorded assessments. A 90-day/180-day flag describes evidence age, not an automatic legal expiry. No data is transmitted.','cc-footnote');host.append(footer);
 return summary;
}
