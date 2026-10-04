export const serialize = data => JSON.stringify(data);
export const empty = () => ({version:1, records:[], updatedAt:null});
export function validate(data, catalog) {
 if(!data || data.version!==1 || !Array.isArray(data.records)||data.records.length>5000) throw Error('Use a version 1 suite export with at most 5,000 records.');
 if(new TextEncoder().encode(JSON.stringify(data)).length>20*1024*1024)throw Error('Dataset exceeds the 20 MB capacity.');
 const ids=new Set();
 for(const r of data.records){
  if(r.domainSlug&&catalog.domains&&!catalog.domains.some(d=>d.slug===r.domainSlug))throw Error('Unknown governance domain.');
  const fields=catalog.entities[r.type]; if(!fields)throw Error('Unknown record type.');
  if(typeof r.id!=='string'||!/^[A-Za-z0-9_-]{1,64}$/.test(r.id)||ids.has(r.id))throw Error('IDs must be unique and contain letters, numbers, underscores or hyphens.');ids.add(r.id);
  if(typeof r.title!=='string'||!r.title.trim())throw Error('Every record needs a title.');
  for(const [k,v] of Object.entries(r)){
   if(k==='type')continue; const t=fields[k];if(!t)throw Error('Unknown field: '+k);
   if(v===''||v===null)continue;
   if(Array.isArray(t)){if(!t.includes(v))throw Error('Invalid '+k);}
   else if(['number','score','percent'].includes(t)){if(typeof v!=='number'||!Number.isFinite(v)||v<0|| (t==='score'&&(!Number.isInteger(v)||v<1||v>5))||(t==='percent'&&v>100))throw Error('Invalid numeric value for '+k);}
   else if(t==='boolean'){if(typeof v!=='boolean')throw Error('Invalid boolean.');}
   else {if(typeof v!=='string'||v.length>4000)throw Error('Invalid text field.');if(t==='date'&&!/^\d{4}-\d{2}-\d{2}$/.test(v))throw Error('Dates must use YYYY-MM-DD.');if(t==='date'&&(isNaN(Date.parse(v))||new Date(v).toISOString().slice(0,10)!==v))throw Error('Invalid calendar date.');if(t==='url'){let url;try{url=new URL(v);}catch{throw Error('Evidence links must be valid HTTPS URLs.');}if(url.protocol!=='https:'||!url.hostname)throw Error('Evidence links must use valid HTTPS URLs.');}}
  }
  for(const count of ['evaluationTotal','evaluationFailed','testedCount','populationSize','attested','requiredAttestations'])if(typeof r[count]==='number'&&!Number.isInteger(r[count]))throw Error('Counts must be whole numbers.');
  if(r.evaluationFailed>r.evaluationTotal||r.testedCount>r.populationSize||r.attested>r.requiredAttestations)throw Error('Completed/failed counts cannot exceed total counts.');
  if(r.result==='Pass'&&(!r.evidenceURL||!r.reviewer?.trim()||!r.testedDate))throw Error('Passing tests require evidence, reviewer and test date.');
  if(r.closedDate&&r.openedDate&&r.closedDate<r.openedDate)throw Error('Closure cannot precede opening.');
 }
 const byId=new Map(data.records.map(r=>[r.id,r]));
 for(const r of data.records)for(const [k,t]of Object.entries(catalog.entities[r.type]))if(typeof t==='string'&&t.startsWith('ref:')&&r[k]){
  const target=byId.get(r[k]);if(!target||target.type!==t.slice(4)||target.id===r.id)throw Error('Invalid linked record: '+k);
 }
 for(const key of ['parentVendorId','dependencyId']){const done=new Set();for(const r of data.records){if(done.has(r.id))continue;const active=new Set();let n=r;while(n&&!done.has(n.id)){if(active.has(n.id))throw Error('Circular dependency.');active.add(n.id);n=n[key]?byId.get(n[key]):null;}for(const id of active)done.add(id);}}
 return structuredClone(data);
}
export function metrics(records,asOf,linkedRecords=records){
 const risk=records.filter(x=>x.type==='risk'),controls=records.filter(x=>x.type==='control');
 const currentPass=linkedRecords.filter(x=>x.type==='test'&&x.result==='Pass'&&x.testedDate<=asOf&&x.expiresDate&&x.expiresDate>=asOf);
 const covered=controls.filter(c=>currentPass.some(t=>t.controlId===c.id)).length;
 return {total:records.length,overdue:records.filter(x=>x.reviewDate&&x.reviewDate<asOf&&x.status!=='Closed').length,openIssues:records.filter(x=>x.type==='issue'&&x.status!=='Closed').length,coverage:controls.length?Math.round(100*covered/controls.length):null,covered,controls:controls.length,highRisk:risk.filter(x=>x.likelihood*x.impact>=15).length,heat:Array.from({length:25},(_,i)=>risk.filter(x=>x.likelihood===Math.floor(i/5)+1&&x.impact===i%5+1).length)};
}
export function score(r){return r.type==='risk'&&r.likelihood&&r.impact?r.likelihood*r.impact:null;}
export function related(records,id){return records.filter(r=>r.id!==id&&Object.entries(r).some(([k,v])=>k.endsWith('Id')&&v===id));}

export function derived(r,records,asOf=new Date().toISOString().slice(0,10)){
 const n=x=>typeof x==='number';const rate=(a,b)=>n(a)&&n(b)&&b>0?Math.round(a/b*1000)/10+'%':'—';
 const days=(start,end)=>start&&end?Math.floor((Date.parse(end)-Date.parse(start))/86400000):null;
 if(r.type==='obligation')return 'Mapped controls '+records.filter(x=>x.type==='control'&&x.obligationId===r.id).length;
 if(r.type==='control'){const tests=records.filter(x=>x.type==='test'&&x.controlId===r.id);return 'Tests '+tests.length+' · Current passes '+tests.filter(x=>x.result==='Pass'&&x.testedDate<=asOf&&x.expiresDate>=asOf).length;}
 if(r.type==='issue'){const age=days(r.openedDate,r.closedDate||asOf);return age===null?'Age —':'Age '+age+' days';}
 if(r.type==='test')return r.expiresDate?(r.expiresDate<asOf?'Evidence expired':r.testedDate>asOf?'Test scheduled':'Evidence validity: '+days(asOf,r.expiresDate)+' days'):'Expiry not set';
 if(r.type==='asset')return 'Criticality '+(r.criticality??'—')+' · '+(r.patchStatus==='Pending'&&r.criticality>=4?'Priority patch review':r.patchStatus||'Patch status not set');
 if(r.type==='decision')return 'Assigned RACI '+['responsible','accountable','consulted','informed'].filter(k=>r[k]).length+'/4';
 if(r.type==='processing')return 'Defined fields '+['purpose','lawfulBasis','dataCategories','retentionDays','transferMechanism'].filter(k=>r[k]!==undefined&&r[k]!==null&&r[k]!=='').length+'/5';
 if(r.type==='risk')return 'Inherent '+(score(r)??'—')+' · Residual '+(r.residualLikelihood&&r.residualImpact?r.residualLikelihood*r.residualImpact:'—');
 if(r.type==='vendor'){const refs=records.filter(x=>['asset','contract','processing','ai'].includes(x.type)&&x.vendorId);return 'Dependency share '+rate(refs.filter(x=>x.vendorId===r.id).length,refs.length);}
 if(['metric','contract'].includes(r.type)){const a=r.type==='metric'?r.value:r.slaActual,b=r.type==='metric'?r.threshold:r.slaTarget;return n(a)&&n(b)&&['At most','At least'].includes(r.direction)?((r.direction==='At most'?a<=b:a>=b)?'Within threshold':'Threshold breached'):'—';}
 if(r.type==='audit')return 'Tested '+rate(r.testedCount,r.populationSize);
 if(r.type==='ai')return 'Evaluation failures '+rate(r.evaluationFailed,r.evaluationTotal);
 if(r.type==='policy')return 'Attested '+rate(r.attested,r.requiredAttestations);
 if(r.type==='initiative')return n(r.budgetUSD)&&n(r.spentUSD)?'Budget remaining USD '+(r.budgetUSD-r.spentUSD):'—';
 if(r.type==='assessment')return n(r.currentLevel)&&n(r.targetLevel)?'Target gap '+(r.targetLevel-r.currentLevel):'—';
 return '—';
}
