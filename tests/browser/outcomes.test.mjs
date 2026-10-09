import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {evaluateScenario} from '../../site/assets/scenario-core.mjs';
const read=p=>JSON.parse(fs.readFileSync(new URL('../../'+p,import.meta.url)));
const config=read('content/domain-reviews.json'),catalog=read('content/suite-catalog.json');
const run=path=>evaluateScenario(read(path),config,catalog);

test('curated client scenarios are computed by the canonical 29-domain evaluator',()=>{
 const vendor=run('site/samples/ai-governance/1.json');
 const audit=run('site/samples/audit-readiness/2.json');
 const incident=run('site/samples/processor-governance/3.json');
 assert.equal(vendor.decisionLabMetrics.rows[0].priority,24);
 assert.equal(vendor.decisionLabMetrics.rows[0].band,'High');
 assert.notEqual(vendor.domainReview.readiness.gate,'Ready for accountable review');
 assert.equal(audit.domainReview.readiness.percent,100);
 assert.equal(audit.workspaceMetrics.coverage,100);
 assert.equal(audit.workspaceMetrics.openIssues,0);
 assert.equal(audit.domainReview.findings.length,0);
 assert.equal(incident.decisionLabMetrics.rows[0].priority,20);
 assert.equal(incident.notification.deadlineAt,'2026-10-12T09:00:00.000Z');
 assert.match(incident.notification.applicability,/must confirm/);
 assert.deepEqual(run('site/samples/processor-governance/3.json'),incident);
 for(const result of [vendor,audit,incident]){
  assert.equal(result.schemaVersion,2);
  assert.equal(result.decision,'Not authorized; human decision required');
  assert.match(result.provenance,/Synthetic/);
 }
});

test('client outcome walkthrough links to reproducible fixtures and does not assert verified compliance',()=>{
 const html=fs.readFileSync(new URL('../../site/outcomes/index.html',import.meta.url),'utf8');
 for(const id of ['D14-1','D07-2','D12-3'])assert.ok(html.includes('data-outcome-select="'+id+'"'));
 for(const url of ['/samples/ai-governance/1.json','/samples/audit-readiness/2.json','/samples/processor-governance/3.json','/assets/outcomes.mjs'])assert.ok(html.includes(url));
 assert.match(html,/not fetched|not assert/i);
});
