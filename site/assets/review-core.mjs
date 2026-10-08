import {assess} from './domain-assessment.mjs';
export function review(config, input) {
 const findings=[], validDate=v=>/^\d{4}-\d{2}-\d{2}$/.test(v||'')&&!isNaN(Date.parse(v))&&new Date(v).toISOString().slice(0,10)===v;
 for(const [key,label] of [['scope','Review scope'],['owner','Accountable owner'],['reviewer','Human reviewer']])if(!input[key]?.trim())findings.push({code:key,priority:'Required',finding:label+' is missing',nextAction:'Record '+label.toLowerCase()+'.'});
 const dateValid=validDate(input.asOf)&&validDate(input.expires);
 if(!dateValid)findings.push({code:'evidence-date',priority:'Required',finding:'Reporting date and evidence validity must be valid calendar dates',nextAction:'Confirm both dates against the review period.'});
 else if(input.expires<input.asOf)findings.push({code:'evidence-expired',priority:'High',finding:'Evidence is expired at the reporting date',nextAction:'Obtain and review current evidence before relying on it.'});
 let urlValid=false;try{const u=new URL(input.evidenceURL);urlValid=u.protocol==='https:'&&!u.username&&!u.password;}catch{}
 if(!urlValid)findings.push({code:'evidence-source',priority:'Required',finding:'A valid HTTPS evidence reference is missing',nextAction:'Link an authorized evidence source; exclude credentials from the URL.'});
 const assessment=assess(config,input.domainInputs);if(assessment)findings.push(...assessment.findings);
 const completed=config.checks.filter((_,i)=>input.checks?.[i]===true).length;
 config.checks.forEach((text,i)=>{if(input.checks?.[i]!==true)findings.push({code:'domain-check-'+(i+1),priority:'Review',finding:text+' — not confirmed',nextAction:'Obtain supporting evidence and reviewer confirmation.'});});

 return {schemaVersion:2,assessment,domain:config.slug,title:config.title,scope:input.scope?.trim()||'',owner:input.owner?.trim()||'',reviewer:input.reviewer?.trim()||'',reportingDate:input.asOf||'',evidence:{url:input.evidenceURL||'',validUntil:input.expires||'',referenceValid:urlValid,contentVerified:false},frameworks:config.frameworks,checks:config.checks.map((label,i)=>({label,confirmed:input.checks?.[i]===true})),readiness:{confirmed:completed,total:config.checks.length,percent:Math.round(completed/config.checks.length*100),gate:findings.length?'Hold pending evidence and review':'Ready for accountable review'},upstream:config.upstream,downstream:config.downstream,findings,decision:'Not authorized; human decision required'};
}
