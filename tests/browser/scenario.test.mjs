import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {evaluateScenario} from '../../site/assets/scenario-core.mjs';
import {scenarioInput} from '../../server/scenario-runtime.mjs';
const root=new URL('../../',import.meta.url),read=p=>JSON.parse(fs.readFileSync(new URL(p,root)));
const configs=read('content/domain-reviews.json'),catalog=read('content/suite-catalog.json'),index=read('content/scenarios-index.json');
const load=x=>read('site'+x.url),evaluate=x=>evaluateScenario(x,configs,catalog);
test('Every domain has three reproducible, distinct, schema-valid delivery scenarios',()=>{
 assert.equal(index.length,configs.length*3);
 for(const c of configs){const items=index.filter(x=>x.domain===c.slug);assert.equal(items.length,3);const results=items.map(x=>{const value=load(x),result=evaluate(value);assert.equal(result.domainReview.readiness.gate,x.expectedGate);assert.deepEqual(evaluate(value),result);assert.deepEqual(result.workspace,value.workspace);assert.deepEqual(result.decisionLab,value.decisionLab);assert.deepEqual(result.domainReview.upstream,c.upstream);assert.deepEqual(result.domainReview.downstream,c.downstream);assert.ok(result.workspace.records.some(r=>r.domainSlug===c.slug));return result;});
  assert.deepEqual(results.map(r=>r.decisionLabMetrics.rows[0].priority),[24,2,20]);assert.equal(results[1].workspaceMetrics.coverage,100);assert.equal(results[1].domainReview.readiness.percent,100);assert.equal(results[1].domainReview.findings.length,0);assert.equal(results[2].notification.deadlineAt,'2026-10-12T09:00:00.000Z');assert.equal(results[0].notification,null);
 }
});
test('Scenario API uses the same deterministic browser contract and requires authorization',()=>{const value=load(index[0]);assert.deepEqual(scenarioInput({scenario:value,authorized:true}),evaluate(value));assert.throws(()=>scenarioInput({scenario:value,authorized:false}));assert.throws(()=>scenarioInput({scenario:value,authorized:true,tenant:'spoof'}));});
test('Invalid fields, native reference collisions, incompatible snapshots and bad assertions are rejected',()=>{
 const mutations=[x=>x.extra='dropped?',x=>x.workspace.extra='dropped?',x=>x.decisionLab.extra='dropped?',x=>x.reviewInputs.domainInputs.extra=4,x=>x.reviewInputs.domainInputs.population=null,x=>x.reviewInputs.checks=['yes'],x=>x.workspace.records[1].obligationId='missing',x=>x.workspace.records.push(x.workspace.records[0]),x=>x.decisionLab.asOf='2026-10-10',x=>x.decisionLab.records[0].parentVendorId=x.decisionLab.records[0].id,x=>x.context='x'.repeat(17000)];
 for(const mutate of mutations){const value=load(index[0]);mutate(value);assert.throws(()=>evaluate(value));}
 const incident=load(index[2]);incident.incident.awareAt='2026-02-30T09:00:00Z';assert.throws(()=>evaluate(incident));
});

test('Authenticated Pages API evaluates and caches a scenario without invoking a model',async()=>{
 const {onRequestPost}=await import('../../functions/api/evaluate.js');
 const keys=await crypto.subtle.generateKey({name:'RSASSA-PKCS1-v1_5',modulusLength:2048,publicExponent:new Uint8Array([1,0,1]),hash:'SHA-256'},true,['sign','verify']);
 const jwk=await crypto.subtle.exportKey('jwk',keys.publicKey);jwk.kid='scenario-key';const issuer='https://scenario.cloudflareaccess.com/';
 const b64=x=>Buffer.from(x).toString('base64url');const header=b64(JSON.stringify({alg:'RS256',kid:jwk.kid})),body=b64(JSON.stringify({iss:issuer,aud:['scenario-app'],sub:'reviewer',exp:Math.floor(Date.now()/1000)+300}));const sig=await crypto.subtle.sign('RSASSA-PKCS1-v1_5',keys.privateKey,new TextEncoder().encode(header+'.'+body));const jwt=header+'.'+body+'.'+b64(sig);
 let stored=null,reservations=0;const env={ACCESS_ISSUER:issuer,ACCESS_AUDIENCE:'scenario-app',GRC_DB:{prepare(sql){return {bind(...args){return {async first(){if(sql.includes('FROM members'))return {tenant_id:'t1',name:'Example organization',allowance:2};if(sql.includes('input_hash'))return stored;return null;},async run(){if(sql.startsWith('INSERT')){reservations++;stored={input_hash:args[2],status:'pending',report:null};}if(sql.includes("status='complete'")){stored.status='complete';stored.report=args[0];}return {meta:{changes:1}};}};}};}}};
 const original=globalThis.fetch;globalThis.fetch=async url=>{assert.match(String(url),/\/cdn-cgi\/access\/certs$/);return new Response(JSON.stringify({keys:[jwk]}));};
 try{const request=value=>new Request('https://example.test/api/evaluate',{method:'POST',headers:{Origin:'https://example.test','Content-Type':'application/json','Cf-Access-Jwt-Assertion':jwt,'Idempotency-Key':'scenario-request-0001'},body:JSON.stringify({scenario:value,authorized:true})});
  const response=await onRequestPost({request:request(load(index[0])),env});assert.equal(response.status,200);assert.deepEqual(await response.json(),evaluate(load(index[0])));
  assert.equal((await onRequestPost({request:request(load(index[0])),env})).status,200);assert.equal(reservations,1);
  assert.equal((await onRequestPost({request:request(load(index[1])),env})).status,409);
 }finally{globalThis.fetch=original;}
});
