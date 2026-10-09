import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {executiveMetrics,executiveMemo,RISK_HIGH,RISK_MODERATE} from '../../site/assets/dashboard-core.mjs';
import {evaluateScenario} from '../../site/assets/scenario-core.mjs';
const read=path=>JSON.parse(fs.readFileSync(new URL('../../'+path,import.meta.url)));
const configs=read('content/domain-reviews.json'),catalog=read('content/suite-catalog.json');
const scenario=path=>evaluateScenario(read('site/samples/'+path),configs,catalog);
test('risk matrix is 5 by 5, user appetite is explicit and unassessed residual risk stays visible',()=>{
 const records=[
  {type:'risk',id:'R1',title:'Supplier breach',domainSlug:'vendor-risk',owner:'Risk owner',likelihood:4,impact:4,residualLikelihood:2,residualImpact:5,exposureUSD:10000},
  {type:'risk',id:'R2',title:'Unassessed exposure',domainSlug:'ai-governance',likelihood:3,impact:3},
  {type:'risk',id:'R3',title:'No residual',domainSlug:'ai-governance',likelihood:1,impact:1}
 ];
 const m=executiveMetrics(records,'2026-10-10',{appetite:9});
 assert.equal(m.heat.length,25);
 assert.equal(m.heat.reduce((n,c)=>n+c.count,0),3);
 assert.equal(m.heat.find(c=>c.likelihood===4&&c.impact===4).count,1);
 assert.equal(m.highInherent,1);
 assert.equal(m.aboveAppetite,1);
 assert.equal(m.unassessedResidual,2);
 assert.equal(m.riskRows[0].residual,10);
 assert.equal(RISK_HIGH,16);assert.equal(RISK_MODERATE,9);
 assert.equal(executiveMetrics(records,'2026-10-10',{domain:'vendor-risk'}).risks,1);
 assert.throws(()=>executiveMetrics(records,'2026-10-10',{appetite:0}));
});
test('control freshness, expired tests, cross-domain evidence and framework mapping remain distinct',()=>{
 const rows=[
 {type:'obligation',id:'O',title:'Independent assurance',framework:'SOC 2',domainSlug:'audit-readiness'},
 {type:'control',id:'C',title:'User access',obligationId:'O',domainSlug:'audit-readiness'},
 {type:'test',id:'T',title:'Passing test',controlId:'C',result:'Pass',evidenceURL:'https://example.com/evidence',reviewer:'Reviewer',testedDate:'2026-07-01',expiresDate:'2026-10-15',domainSlug:'internal-audit'},
 {type:'issue',id:'I',title:'Access incident',category:'Incident',owner:'SecOps',status:'Open',reviewDate:'2026-10-01',severity:'High',correctiveAction:'Review access',domainSlug:'audit-readiness'}
 ];
 const m=executiveMetrics(rows,'2026-10-10',{domain:'audit-readiness'});
 assert.equal(m.controlPass,1);assert.equal(m.controlCoverage,100);
 assert.equal(m.evidenceAges.older90,1);assert.equal(m.openIncidents,1);assert.equal(m.overdue,1);
 assert.equal(m.frameworks[0].tested,1);
 const expired=executiveMetrics(rows,'2026-10-16',{domain:'audit-readiness'});
 assert.equal(expired.controlCoverage,0);
 assert.equal(expired.controlStates[0].status,'Expired evidence');
 assert.match(executiveMemo(expired),/not real-time system telemetry/);
});
test('all three bundled demos produce distinct in-browser summary values',()=>{
 const vendor=scenario('ai-governance/1.json'),audit=scenario('audit-readiness/2.json'),incident=scenario('processor-governance/3.json');
 for(const p of [vendor,audit,incident]){
  const m=executiveMetrics(p.workspace.records,p.domainReview.reportingDate);
  assert.equal(m.records,p.workspace.records.length);
  assert.equal(m.controlCoverage,p.workspaceMetrics.coverage);
  assert.ok(m.heat.length===25);
 }
 assert.equal(vendor.decisionLabMetrics.rows[0].priority,24);
 assert.equal(audit.domainReview.readiness.percent,100);
 assert.equal(incident.notification.deadlineAt,'2026-10-12T09:00:00.000Z');
});
test('all 29 generated routes have download/import walkthrough, console-free module syntax and control center links',()=>{
 const projects=read('content/projects.json');
 assert.equal(projects.length,29);
 for(const p of projects){
  const html=fs.readFileSync(new URL('../../site/work/'+p.slug+'/index.html',import.meta.url),'utf8');
  assert.match(html,/assets\/scenario-ui\.mjs/);
  assert.match(html,/\/control-center\//);
 }
 const route=fs.readFileSync(new URL('../../site/control-center/index.html',import.meta.url),'utf8');
 assert.match(route,/id="cc-import"/);
 assert.match(route,/id="cc-dashboard"/);
 const src=fs.readFileSync(new URL('../../site/assets/scenario-ui.mjs',import.meta.url),'utf8');
 assert.doesNotMatch(src,/confirm\(/);
 assert.match(src,/scenario-apply/);
 assert.match(src,/Scenario loaded successfully/);
});
