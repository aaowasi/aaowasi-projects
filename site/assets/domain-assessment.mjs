// Metadata calculations do not verify evidence content or make legal decisions.
export function assess(config, values = {}) {
 const a=config.assessment, findings=[];if(!a)return null;
 const numbers=a.fields.filter(f=>f.type==='number');
 for(const f of numbers){const raw=values[f.key];const n=Number(raw);if(raw===undefined||raw===''||!Number.isFinite(n)||n<f.min||n>f.max||!Number.isInteger(n))findings.push({code:'assessment-'+f.key,priority:'Required',finding:f.label+' must be a whole number between '+f.min+' and '+f.max,nextAction:'Confirm the defined population, unit and reporting period.'});}
 if(values.approval!=='Confirmed')findings.push({code:'assessment-approval',priority:'Review',finding:a.fields[2].label+' — not confirmed',nextAction:a.action});
 const population=Number(values.population),baseline=Number(values.baseline);let metric=null;
 if(!findings.some(f=>f.code==='assessment-population'||f.code==='assessment-baseline')){
  if(a.mode==='coverage'){
   if(population===0||baseline>population)findings.push({code:'assessment-population-consistency',priority:'Required',finding:'Use a nonzero scoped population and a completed count no larger than it',nextAction:'Correct the population or document non-applicability outside this assessment.'});
   else {metric={covered:baseline,total:population,uncovered:population-baseline,coveragePercent:Math.round(baseline/population*100)};if(baseline<population)findings.push({code:'assessment-gap',priority:'Review',finding:(population-baseline)+' scoped items require completion',nextAction:a.action});}
  }else{
   metric={observed:population,threshold:baseline,excess:Math.max(0,population-baseline),unit:a.mode==='deadline'?'declared time unit':a.mode==='recovery'?'minutes':'declared domain unit'};
   if(population>baseline)findings.push({code:'assessment-threshold',priority:'High',finding:'Observed value exceeds the declared '+(a.mode==='deadline'?'deadline':a.mode==='recovery'?'recovery objective':'tolerance')+' by '+(population-baseline),nextAction:a.action});
  }
 }
 return {deliverable:a.deliverable,method:a.mode,inputs:Object.fromEntries(a.fields.map(f=>[f.key,values[f.key]??null])),metric,acceptance:a.acceptance,findings};
}
export function deliveryMemo(result) {
 const clean=v=>String(v??'Not recorded').replace(/[\r\n]+/g,' ');
 const a=result.assessment;
 return ['# '+clean(a.deliverable),'','Status: '+clean(result.readiness.gate),'Scope: '+clean(result.scope),'Owner: '+clean(result.owner),'Reviewer: '+clean(result.reviewer),'Reporting date: '+clean(result.reportingDate),'','## Domain assessment','Method: '+clean(a.method),...Object.entries(a.inputs).map(([k,v])=>k+': '+clean(v)),'Calculation: '+JSON.stringify(a.metric),'','## Evidence reference',clean(result.evidence.url),'Valid until: '+clean(result.evidence.validUntil),'Content verification: pending accountable reviewer','', '## Findings and actions',...result.findings.map(f=>'- '+clean(f.finding)+'; '+clean(f.nextAction)),'','## Dependency handoffs','Upstream: '+result.upstream.join(', '),'Downstream: '+result.downstream.join(', '),'','## Acceptance',clean(a.acceptance),'Not authorized; this metadata report is not a certification or audit opinion.'].join('\n');
}
