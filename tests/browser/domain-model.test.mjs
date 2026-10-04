import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {domainProjects,domainRecords,domainCounts} from '../../site/assets/domain-core.mjs';
import {validate} from '../../site/assets/suite-core.mjs';
const read=p=>JSON.parse(fs.readFileSync(new URL(p,import.meta.url)));
const projects=read('../../content/projects.json'),catalog=read('../../content/suite-catalog.json');
test('every domain has a unique dedicated project and valid directed handoffs',()=>{
 assert.equal(projects.length,29);assert.equal(new Set(projects.map(p=>p.slug)).size,projects.length);
 assert.deepEqual(new Set(catalog.domains.map(d=>d.slug)),new Set(projects.map(p=>p.slug)));
 for(const p of projects){assert.ok(p.frameworks.length);assert.ok(!p.frameworks.some(f=>/^custom$/i.test(f)));assert.ok(p.upstream.length&&p.downstream.length);for(const slug of p.upstream){const source=projects.find(x=>x.slug===slug);assert.ok(source);assert.ok(source.downstream.includes(p.slug));}}
});
test('all-domain selection preserves every project including the final authorization domain',()=>{
 assert.equal(domainProjects(projects).length,projects.length);assert.equal(domainProjects(projects).at(-1).slug,'ongoing-authorization');assert.equal(domainProjects(projects,'cloud-change').length,1);
 const counts=domainCounts([...catalog.domains,{slug:'future-domain'}],catalog);assert.equal(counts.domains,catalog.domains.length+1);
});
test('perspectives scope classified records without dropping legacy records from All domains',()=>{
 const records=[{id:'A',domainSlug:'cloud-change'},{id:'B',domainSlug:'identity-authorization'},{id:'C'}];assert.equal(domainRecords(records).length,3);assert.deepEqual(domainRecords(records,'cloud-change').map(r=>r.id),['A']);assert.equal(domainRecords(records,'ongoing-authorization').length,0);
});
test('invalid domain assignments fail but cross-domain evidence references remain valid',()=>{
 assert.throws(()=>validate({version:1,records:[{type:'control',id:'C',title:'Control',domainSlug:'missing'}]},catalog));
 const records=[{type:'control',id:'C',title:'Access control',domainSlug:'identity-authorization'},{type:'test',id:'T',title:'Reviewed access evidence',domainSlug:'evidence-integrity',controlId:'C'}];assert.equal(validate({version:1,records},catalog).records.length,2);
});
