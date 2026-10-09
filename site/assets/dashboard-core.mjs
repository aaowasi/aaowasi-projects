/**
 * Deterministic, browser-safe executive risk summary from the 29-domain typed suite.
 * Scores are policy/metadata signals, NOT legal compliance or certification findings.
 */
export const RISK_HIGH=16,RISK_MODERATE=9;
const score=(a,b)=>Number.isInteger(a)&&Number.isInteger(b)&&a>=1&&a<=5&&b>=1&&b<=5?a*b:null;
const band=s=>s===null?'Unassessed':s>=RISK_HIGH?'High':s>=RISK_MODERATE?'Moderate':'Low';
const current=(s,t)=>Boolean(s&&s!=='Closed'&&s!=='Approved')&&(!t||s!=='Closed');
const daysBetween=(a,b)=>Math.floor((Date.parse(b+'T00:00:00Z')-Date.parse(a+'T00:00:00Z'))/86400000);
const allowedDate=x=>typeof x==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(x)&&Number.isFinite(Date.parse(x+'T00:00:00Z'))&&new Date(x+'T00:00:00Z').toISOString().slice(0,10)===x;
export function executiveMetrics(records,asOf,options={}){
 if(!Array.isArray(records)||!allowedDate(asOf))throw Error('Dashboard requires typed records and a valid snapshot date.');
 const appetite=options.appetite??RISK_MODERATE;
 if(!Number.isInteger(appetite)||appetite<1||appetite>25)throw Error('Risk appetite must be between 1 and 25.');
 const domain=options.domain||'';
 const scoped=domain?records.filter(r=>r.domainSlug===domain):records;
 const projected=Array.isArray(options.projectedRisk)?options.projectedRisk.filter(r=>!domain||r.domainSlug===domain):[];
 const risks=[...scoped.filter(r=>r.type==='risk'),...projected].map(r=>{
  const inherent=score(r.likelihood,r.impact),residual=score(r.residualLikelihood,r.residualImpact);
  return {id:r.id,title:r.title,owner:r.owner||'Unassigned',domain:r.domainSlug||'Unclassified',inherent,residual,inherentBand:band(inherent),residualBand:band(residual),likelihood:r.likelihood,impact:r.impact,exposureUSD:Number.isFinite(r.exposureUSD)?r.exposureUSD:null,aboveAppetite:residual!==null?residual>=appetite:null};
 });
 risks.sort((a,b)=>(b.residual??b.inherent??-1)-(a.residual??a.inherent??-1)||a.id.localeCompare(b.id));
 const heat=Array.from({length:25},(_,i)=>{
  const likelihood=5-Math.floor(i/5),impact=i%5+1;
  return {likelihood,impact,score:likelihood*impact,band:band(likelihood*impact),count:risks.filter(x=>x.likelihood===likelihood&&x.impact===impact).length};
 });
 const controls=scoped.filter(r=>r.type==='control');
 const ids=new Set(controls.map(r=>r.id));
 // In scoped dashboard, a cross-domain test still belongs to its linked control.
 const tests=records.filter(r=>r.type==='test'&&ids.has(r.controlId));
 const byControl=new Map();
 for(const t of tests){const x=byControl.get(t.controlId)||[];x.push(t);byControl.set(t.controlId,x);}
 const controlStates=controls.map(c=>{
  const results=byControl.get(c.id)||[];
  const passing=results.some(t=>t.result==='Pass'&&allowedDate(t.testedDate)&&t.testedDate<=asOf&&allowedDate(t.expiresDate)&&t.expiresDate>=asOf&&t.reviewer?.trim()&&t.evidenceURL?.startsWith('https://'));
  const failed=results.some(t=>t.result==='Fail'&&allowedDate(t.testedDate)&&t.testedDate<=asOf);
  const expired=results.some(t=>allowedDate(t.expiresDate)&&t.expiresDate<asOf);
  const recent=results.filter(t=>allowedDate(t.testedDate)&&t.testedDate<=asOf).map(t=>daysBetween(t.testedDate,asOf));
  return {id:c.id,title:c.title,owner:c.owner||'Unassigned',status:passing?'Recorded pass':failed?'Recorded failure':expired?'Expired evidence':'Not evidenced',passing,failed,expired,ageDays:recent.length?Math.min(...recent):null};
 });
 const tested=controlStates.filter(c=>c.passing).length;
 const issues=scoped.filter(r=>r.type==='issue'&&r.status!=='Closed');
 const overdue=scoped.filter(r=>r.status!=='Closed'&&allowedDate(r.reviewDate)&&r.reviewDate<asOf);
 const incidents=issues.filter(r=>(r.category||'').toLowerCase().includes('incident'));
 const obligations=scoped.filter(r=>r.type==='obligation');
 const frameworks=new Map();
 for(const o of obligations){const framework=(o.framework||'Unclassified').trim()||'Unclassified';
  const f=frameworks.get(framework)||{name:framework,obligations:0,mapped:0,tested:0};
  const linked=controls.filter(c=>c.obligationId===o.id);
  f.obligations++;if(linked.length)f.mapped++;
  if(linked.length&&linked.every(c=>controlStates.some(s=>s.id===c.id&&s.passing)))f.tested++;
  frameworks.set(framework,f);
 }
 const above=risks.filter(r=>r.aboveAppetite===true);
 const missingResidual=risks.filter(r=>r.residual===null);
 const evidenceAges={older90:controlStates.filter(x=>x.ageDays!==null&&x.ageDays>90).length,older180:controlStates.filter(x=>x.ageDays!==null&&x.ageDays>180).length};
 return {asOf,domain:domain||'All domains',appetite,records:scoped.length,risks:risks.length,
  topRisks:risks.slice(0,8),riskRows:risks,heat,
  appetiteStatus:above.length?'Above appetite':missingResidual.length?'Incomplete assessments':risks.length?'Within declared threshold':'No risk assessments',
  aboveAppetite:above.length,unassessedResidual:missingResidual.length,
  highInherent:risks.filter(r=>r.inherent!==null&&r.inherent>=RISK_HIGH).length,
  highResidual:risks.filter(r=>r.residual!==null&&r.residual>=RISK_HIGH).length,
  controlTotal:controls.length,controlPass:tested,controlFail:controlStates.filter(c=>c.failed&&!c.passing).length,
  controlCoverage:controls.length?Math.round(tested/controls.length*100):null,
  evidenceAges,controlStates,
  openIssues:issues.length,openIncidents:incidents.length,overdue:overdue.length,
  issues:issues.slice(0,20).map(x=>({id:x.id,title:x.title,owner:x.owner||'Unassigned',severity:x.severity||'Not classified',category:x.category||'Issue',action:x.correctiveAction||'Needs owner action'})),
  overdueItems:overdue.slice(0,20).map(x=>({id:x.id,title:x.title,owner:x.owner||'Unassigned',reviewDate:x.reviewDate})),
  frameworks:[...frameworks.values()].sort((a,b)=>a.name.localeCompare(b.name))
 };
}
export function executiveMemo(m){
 const percent=m.controlCoverage===null?'N/A':m.controlCoverage+'%';
 const lines=['# Executive technology risk & GRC decision brief','',`Snapshot: ${m.asOf} | Perspective: ${m.domain}`,`Illustrative residual risk appetite threshold: ${m.appetite}/25 (editable; not an organization-approved policy)`,'',
 '## Executive indicators',`Risks: ${m.risks}; inherent high (≥16): ${m.highInherent}; residual high (≥16): ${m.highResidual}`,`Above threshold: ${m.aboveAppetite}; missing residual assessments: ${m.unassessedResidual}`,`Recorded passing controls: ${m.controlPass}/${m.controlTotal} (${percent})`,`Open issues: ${m.openIssues}; incident-classified issues: ${m.openIncidents}; overdue reviews/actions: ${m.overdue}`,`Evidence >90 days: ${m.evidenceAges.older90}; >180 days: ${m.evidenceAges.older180}`,'',
 '## Highest-priority risks',...m.topRisks.map(r=>`- ${r.id} [${r.domain}]: ${r.title} — inherent ${r.inherent??'N/A'}, residual ${r.residual??'unassessed'}, owner ${r.owner}`),'',
 '## Immediate action queue',...m.issues.slice(0,10).map(x=>`- ${x.id}: ${x.action} (owner: ${x.owner})`),'',
 '## Framework-linked obligations (not statutory compliance scores)',...m.frameworks.map(x=>`- ${x.name}: ${x.tested}/${x.obligations} obligations with mapped controls and recorded passing tests`),'',
 '## Evidence boundary','Risk and test calculations use the imported metadata, not real-time system telemetry. Evidence URLs are not fetched or verified. A human reviewer must confirm legal applicability, completeness, scope and release authorization.',''];
 return lines.join('\n');
}

/**
 * UI-only join. Scenario Decision Lab scores must be visible in the executive
 * heatmap without manufacturing typed risk records in an editable V1 export.
 * These projections have no residual assessment and are NEVER auto-approved.
 */
export function projectScenarioRisks(pack){
 if(!pack||pack.schemaVersion!==2||!Array.isArray(pack.decisionLab?.records))return [];
 return pack.decisionLab.records.map(r=>({
  type:'risk',id:'LAB-'+r.id,title:r.name+' · synthetic Decision Lab',
  owner:r.owner||'Example reviewer unassigned',domainSlug:pack.domain,
  likelihood:r.likelihood,impact:r.impact
 }));
}
