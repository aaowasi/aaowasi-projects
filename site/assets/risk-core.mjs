/** Browser-local portfolio policy. No regulatory score or automated legal conclusion. */
export const VERSION='1.0';
export const FIELDS=['id','name','owner','service','criticality','dataSensitivity','ai','approved','processor','region','dpa','transfer','disclosure','oversight','evidence','likelihood','impact','treatment','reviewer','rationale','parentVendorId','controlId','evidenceRef','testOutcome','evidenceReviewedAt','evidenceExpiresAt','question','aiEvalTotal','aiEvalFailed','techniqueId'];
export const ENUMS={testOutcome:['not-tested','pass','fail','error'],criticality:['low','medium','high'],dataSensitivity:['public','internal','personal','sensitive'],region:['EEA','UK','US','Other'],evidence:['missing','current','stale','failed','error'],treatment:['unreviewed','mitigate','accept','avoid'],disclosure:['unreviewed','tested','gap'],oversight:['unreviewed','assigned','tested']};
export const BOOLS=['ai','approved','processor','dpa','transfer'];
export const MAX_RECORDS=250,MAX_BYTES=10000000;
const own=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
export function empty(){return {schemaVersion:VERSION,asOf:'2026-09-24',provenance:'User supplied; not independently verified',assumptions:{manualMinutes:90,assistedMinutes:35,hourlyCost:80,setupCost:1200},records:[]};}
export function validate(input){
 if(!input||typeof input!=='object'||Array.isArray(input)||input.schemaVersion!==VERSION)throw Error('Expected workspace schemaVersion 1.0.');
 if(!Array.isArray(input.records)||input.records.length>MAX_RECORDS)throw Error('records must be an array of at most 250 records.');
 const asOf=input.asOf;
 if(!validDate(asOf))throw Error('asOf must be a real YYYY-MM-DD snapshot date.');
 const seen=new Set();const records=input.records.map((r,i)=>{
  const fail=m=>{throw Error(`Row ${i+1}: ${m}`)};
  if(!r||typeof r!=='object'||Array.isArray(r))fail('expected a record.');
  for(const k of Object.keys(r))if(!FIELDS.includes(k))fail(`unsupported field ${k}; remove extra fields, including raw prompts or secrets.`);
  const out={};
  for(const k of FIELDS){if(!own(r,k))fail(`missing ${k}.`);const v=r[k];
   if(BOOLS.includes(k)){if(typeof v!=='boolean')fail(`${k} must be true or false.`);out[k]=v;}
   else if(k==='aiEvalTotal'||k==='aiEvalFailed'){if(!Number.isInteger(v)||v<0||v>100000)fail(`${k} must be an integer from 0 to 100000.`);out[k]=v;}
   else if(k==='likelihood'||k==='impact'){if(!Number.isInteger(v)||v<1||v>5)fail(`${k} must be an integer from 1 to 5.`);out[k]=v;}
   else {if(typeof v!=='string'||v.length>300||/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(v))fail(`${k} must be text of at most 300 characters.`);out[k]=v.trim();if(ENUMS[k]&&!ENUMS[k].includes(v))fail(`invalid ${k}.`);}
  }
  if(!/^[A-Za-z0-9_-]{1,40}$/.test(out.id)||seen.has(out.id))fail('id must be unique, 1–40 letters, digits, underscores or hyphens.');seen.add(out.id);
  for(const k of ['name','owner','service'])if(!out[k])fail(`${k} is required.`);
  if(out.aiEvalFailed>out.aiEvalTotal)fail('failed evaluations cannot exceed total.');
  if(out.techniqueId&&!['AML.T0051','AML.T0051.000','AML.T0051.001','AML.T0054','AML.T0020'].includes(out.techniqueId))fail('techniqueId must match the documented ATLAS subset.');
  if(out.aiEvalTotal&&!out.techniqueId)fail('AI evaluations require an ATLAS technique reference.');
  for(const k of ['evidenceReviewedAt','evidenceExpiresAt'])if(out[k]&&!validDate(out[k]))fail(`${k} must be empty or a real YYYY-MM-DD date.`);
  if(out.evidenceReviewedAt>asOf)fail('evidence review date cannot be after the snapshot date.');
  if(out.evidenceReviewedAt&&out.evidenceExpiresAt&&out.evidenceExpiresAt<out.evidenceReviewedAt)fail('expiry cannot precede review date.');
  if(out.evidence==='current'&&(!out.evidenceReviewedAt||!out.evidenceExpiresAt||!out.evidenceRef||!out.controlId))fail('current evidence needs control ID, reference, review date and expiry.');
  if(out.treatment==='accept'&&(!out.reviewer||!out.rationale))fail('risk acceptance needs a reviewer and rationale.');
  return out;
 });
 for(const r of records){if(r.parentVendorId&&!seen.has(r.parentVendorId))throw Error(`${r.id}: parentVendorId must reference an existing record.`);const chain=new Set([r.id]);let parent=r.parentVendorId;while(parent){if(!seen.has(parent))throw Error(`${r.id}: parentVendorId must reference an existing record.`);if(chain.has(parent))throw Error(`${r.id}: dependency cycle detected.`);chain.add(parent);parent=records.find(x=>x.id===parent).parentVendorId;}}
 const a=input.assumptions||empty().assumptions;const assumptions={};
 for(const [k,max] of Object.entries({manualMinutes:10000,assistedMinutes:10000,hourlyCost:10000,setupCost:10000000})){if(typeof a[k]!=='number'||!Number.isFinite(a[k])||a[k]<0||a[k]>max)throw Error(`Invalid assumption ${k}.`);assumptions[k]=a[k];}
 const provenance=typeof input.provenance==='string'?input.provenance.slice(0,300):'User supplied; not independently verified';
 return {schemaVersion:VERSION,asOf,provenance,assumptions,records};
}
export function parseCSV(text){
 if(new TextEncoder().encode(text).length>MAX_BYTES)throw Error('File exceeds 10 MB.');
 const rows=[];let row=[],cell='',quoted=false,closed=false;
 text=text.replace(/^\uFEFF/,'');
 for(let i=0;i<text.length;i++){const c=text[i];
  if(quoted){if(c==='"'){if(text[i+1]==='"'){cell+='"';i++;}else{quoted=false;closed=true;}}else cell+=c;}
  else if(c==='"'){if(cell||closed)throw Error('Malformed CSV quote.');quoted=true;}
  else if(c===','||c==='\n'||c==='\r'){row.push(cell);cell='';closed=false;if(c!==','){if(c==='\r'&&text[i+1]==='\n')i++;if(row.some(x=>x!==''))rows.push(row);row=[];}}
  else {if(closed)throw Error('Unexpected content after closing CSV quote.');cell+=c;}
 }
 if(quoted)throw Error('Unclosed CSV quote.');if(cell||row.length||closed){row.push(cell);rows.push(row);}
 if(!rows.length)throw Error('CSV is empty.');const headers=rows.shift();
 if(headers.length!==FIELDS.length||new Set(headers).size!==headers.length||FIELDS.some(k=>!headers.includes(k)))throw Error('CSV header must contain the exact documented fields. Download the CSV template.');
 const w=empty();w.records=rows.map((r,i)=>{if(r.length!==headers.length)throw Error(`CSV row ${i+2}: wrong column count.`);const out={};headers.forEach((k,j)=>{let v=r[j];if(BOOLS.includes(k)){if(!['true','false'].includes(v))throw Error(`CSV row ${i+2}: ${k} must be true or false.`);v=v==='true';}else if(['aiEvalTotal','aiEvalFailed'].includes(k)){if(!/^\d+$/.test(v))throw Error(`CSV row ${i+2}: ${k} must be a nonnegative integer.`);v=Number(v);}else if(['likelihood','impact'].includes(k)){if(!/^[1-5]$/.test(v))throw Error(`CSV row ${i+2}: ${k} must be 1–5.`);v=Number(v);}out[k]=v;});return out;});return validate(w);
}
export function parseInput(text,filename){if(new TextEncoder().encode(text).length>MAX_BYTES)throw Error('File exceeds 10 MB.');return filename.toLowerCase().endsWith('.csv')?parseCSV(text):validate(JSON.parse(text));}
export function csvCell(v){const s=String(v);return '"'+(/^[\s]*[=+@\-\t\r]/.test(s)?"'"+s:s).replaceAll('"','""')+'"';}
export function toCSV(records){return [FIELDS,...records.map(r=>FIELDS.map(k=>r[k]))].map(row=>row.map(csvCell).join(',')).join('\r\n');}
export function validDate(s){return typeof s==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(s)&&!Number.isNaN(Date.parse(s))&&new Date(s).toISOString().slice(0,10)===s;}
export function score(r,asOf='2026-09-24'){
 const inherent=r.likelihood*r.impact;
 // Risk indicator, not probability: additional flags affect the prioritization score.
 const flags=(r.ai&&!r.approved?3:0)+(r.processor&&!r.dpa?3:0)+(r.processor&&!['EEA','UK'].includes(r.region)&&!r.transfer?2:0);
 const expired=!!r.evidenceExpiresAt&&r.evidenceExpiresAt<asOf;
 const evidenceCurrent=r.evidence==='current'&&!expired;
 const effectiveEvidence=evidenceCurrent?'current':expired&&r.evidence==='current'?'stale':r.evidence;
 const evidenceCredit=evidenceCurrent&&r.testOutcome==='pass'?2:0;
 const priority=Math.min(25,Math.max(1,inherent+flags-evidenceCredit));
 return {inherent,flags,evidenceCredit,priority,expired,evidenceCurrent,effectiveEvidence,evalFailureRate:r.aiEvalTotal?100*r.aiEvalFailed/r.aiEvalTotal:null,band:priority>=16?'High':priority>=9?'Moderate':'Low',aiReview:r.ai&&(r.oversight!=='tested'||r.disclosure!=='tested'||!r.approved||r.aiEvalTotal===0||r.aiEvalFailed>0),privacyGap:r.processor&&(!r.dpa||(!['EEA','UK'].includes(r.region)&&!r.transfer)),releaseReady:r.ai&&r.disclosure==='tested'&&r.oversight==='tested'&&evidenceCurrent&&r.testOutcome==='pass'&&r.approved&&r.aiEvalTotal>0&&r.aiEvalFailed===0,answerReady:evidenceCurrent&&r.testOutcome==='pass'&&!!r.reviewer,egress:r.ai?(!r.approved&&['personal','sensitive'].includes(r.dataSensitivity)?'Block candidate':!r.approved?'Review':'Allow candidate'):'Not AI'};
}
export function derive(w){const rows=w.records.map(r=>({...r,...score(r,w.asOf)}));const n=rows.length;const count=f=>rows.filter(f).length;const a=w.assumptions;const savedHours=n*(a.manualMinutes-a.assistedMinutes)/60;const grossValue=savedHours*a.hourlyCost;return {rows,total:n,ai:count(r=>r.ai),high:count(r=>r.priority>=16),current:count(r=>r.evidenceCurrent),coverage:n?100*count(r=>r.evidenceCurrent)/n:null,expired:count(r=>r.expired),evalTotal:rows.filter(r=>r.ai).reduce((n,r)=>n+r.aiEvalTotal,0),evalFailed:rows.filter(r=>r.ai).reduce((n,r)=>n+r.aiEvalFailed,0),dependencyCounts:Object.fromEntries(rows.map(r=>[r.id,count(x=>x.parentVendorId===r.id)])),aiReviews:count(r=>r.aiReview),privacyGaps:count(r=>r.privacyGap),ready:count(r=>r.answerReady),savedHours,grossValue,netValue:grossValue-a.setupCost,roi:a.setupCost?100*(grossValue-a.setupCost)/a.setupCost:null};}
export function memo(w,module){const d=derive(w);return `AAO | Decision memo\nModule: ${module}\nSchema: ${VERSION}\nSnapshot: ${w.asOf}\nProvenance: ${w.provenance}\n\n${d.total} records; ${d.high} high-priority signals; ${d.aiReviews} AI reviews; ${d.privacyGaps} processor gaps.\nEvidence coverage: ${d.coverage===null?'N/A':d.coverage.toFixed(1)+'%'} (current / all records).\n\nPortfolio policy: priority = min(25, max(1, likelihood × impact + flags − evidence credit)). Flags: unapproved AI +3, missing DPA +3, unresolved non-EEA/UK transfer +2; unexpired current evidence with recorded passing test −2. High >=16; moderate >=9. Not a probability, certification or legal conclusion. UK grouping is a demo triage simplification; all transfers require legal review.\n\nScenario economics, not achieved savings: ${d.savedHours.toFixed(2)} hours = ${d.total} × (${w.assumptions.manualMinutes} − ${w.assumptions.assistedMinutes}) / 60. Gross modeled value ${d.grossValue.toFixed(2)} USD (scenario); setup ${w.assumptions.setupCost}; net ${d.netValue.toFixed(2)}; ROI ${d.roi===null?'N/A':d.roi.toFixed(1)+'%'}.\n\nDecision register\n${d.rows.map(r=>`${r.id} | ${r.name} | owner ${r.owner} | priority ${r.priority} | control ${r.controlId||'unmapped'} | evidence ${r.evidenceRef||'missing'} (${r.effectiveEvidence}) | test ${r.testOutcome} | treatment ${r.treatment} | reviewer ${r.reviewer||'unassigned'} | rationale ${r.rationale||'pending'}`).join('\n')}\n\nHuman action: validate evidence, appoint accountable reviewers, confirm legal applicability and approve any acceptance outside this prototype. Browser-local session edits are not durable audit logs.\n`;}
export function sample(){const w=empty();w.provenance='Synthesized enterprise scenario — fictional records, no observed client outcomes';w.records=[
 ['V01','Cedar Support AI','Service operations','Customer support assistant','high','personal',true,false,true,'US',false,false,'gap','assigned','missing',4,4,'mitigate','',''],
 ['V02','Larch Payroll','People operations','Payroll processing','high','sensitive',false,true,true,'EEA',true,true,'unreviewed','unreviewed','current',3,5,'mitigate','Demo reviewer','Validate sampled access evidence'],
 ['V03','Moor Analytics','Data platform','Product analytics','medium','internal',true,true,true,'UK',true,true,'tested','tested','current',2,3,'unreviewed','Demo reviewer','Review retention configuration'],
 ['V04','Harbor Writer','Marketing','Draft public campaign text','low','public',true,false,false,'US',false,false,'unreviewed','unreviewed','stale',2,2,'unreviewed','',''],
 ['V05','Birch Hosting','Infrastructure','Production hosting','high','personal',false,true,true,'US',true,false,'unreviewed','unreviewed','error',3,5,'mitigate','',''],
 ['V06','Fen Archive','Records management','Document retention','medium','personal',false,true,true,'EEA',false,true,'unreviewed','unreviewed','failed',3,3,'unreviewed','','']
 ].map((values,i)=>({...Object.fromEntries(FIELDS.slice(0,20).map((k,j)=>[k,values[j]])),parentVendorId:["V05","","V05","","",""][i],controlId:['AI-01','IAM-01','AI-02','AUP-01','BCDR-01','RET-01'][i],evidenceRef:['','EV-IAM-012','EV-AI-008','EV-AUP-004','','EV-RET-003'][i],testOutcome:['not-tested','pass','pass','not-tested','error','fail'][i],evidenceReviewedAt:['','2026-09-10','2026-09-12','2026-06-01','','2026-09-18'][i],evidenceExpiresAt:['','2026-12-10','2026-12-12','2026-07-01','','2026-12-18'][i],question:['Has the support assistant been evaluated for prompt injection?','Is payroll access control evidence current?','Has the analytics assistant passed its recorded evaluation?','Is acceptable-use approval documented?','Has the backup restoration control been tested?','Does retention evidence support the policy?'][i],aiEvalTotal:[24,0,30,8,0,0][i],aiEvalFailed:[5,0,0,2,0,0][i],techniqueId:['AML.T0051','','AML.T0051.001','AML.T0054','',''][i]}));return validate(w);}
