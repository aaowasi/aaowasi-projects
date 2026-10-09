import {validate as suiteValidate,metrics} from './suite-core.mjs';
import {validate as labValidate,derive} from './risk-core.mjs';
import {review} from './review-core.mjs';
export const SCENARIO_LIMIT=16000;
const fail=m=>{throw Object.assign(Error(m),{status:400});};
const keys=(v,allowed)=>{if(!v||typeof v!=='object'||Array.isArray(v)||Object.keys(v).some(k=>!allowed.includes(k)))fail('Invalid scenario object or unsupported field.');};
export function evaluateScenario(value,configs,catalog){
 if(new TextEncoder().encode(JSON.stringify(value)).length>SCENARIO_LIMIT)fail('Scenario exceeds 16 KB.');
 keys(value,['scenarioVersion','id','domain','title','context','reviewInputs','workspace','decisionLab','incident']);
 if(value.scenarioVersion!==1||!/^D\d{2}-[123]$/.test(value.id))fail('Expected scenarioVersion 1 and a domain scenario ID.');
 const config=configs.find(c=>c.slug===value.domain);if(!config)fail('Unknown scenario domain.');
 for(const k of ['title','context'])if(typeof value[k]!=='string'||!value[k].trim()||value[k].length>2000)fail('Invalid scenario '+k+'.');
 const input=value.reviewInputs;keys(input,['scope','owner','reviewer','evidenceURL','expires','asOf','checks','domainInputs']);
 for(const k of ['scope','owner','reviewer','evidenceURL','expires','asOf'])if(typeof input[k]!=='string'||input[k].length>1500)fail('Invalid review input '+k+'.');
 keys(input.domainInputs,config.assessment.fields.map(f=>f.key));
 if(!Array.isArray(input.checks)||input.checks.length!==config.checks.length||input.checks.some(x=>typeof x!=='boolean'))fail('Invalid domain assertions.');
 keys(value.workspace,['version','records','updatedAt']);keys(value.decisionLab,['schemaVersion','asOf','provenance','assumptions','records']);keys(value.decisionLab.assumptions,['manualMinutes','assistedMinutes','hourlyCost','setupCost']);for(const f of config.assessment.fields){const v=input.domainInputs[f.key];if(f.type==='number'&&(!Number.isInteger(v)||v<f.min||v>f.max)||f.type==='select'&&!f.options.includes(v))fail('Invalid domain calculation input '+f.key+'.');}
 const workspace=suiteValidate(value.workspace,catalog),decisionLab=labValidate(value.decisionLab);
 if(workspace.records.some(r=>!r.domainSlug))fail('Scenario records require explicit domain ownership.');
 if(workspace.updatedAt!==null&&typeof workspace.updatedAt!=='string')fail('Invalid workspace timestamp.');
 if(input.asOf!==decisionLab.asOf)fail('Review and Decision Lab snapshot dates must agree.');
 const domainReview=review(config,input);
 if(domainReview.findings.some(f=>f.priority==='Required'))fail('Scenario contains invalid or missing review inputs.');
 let notification=null;
 if(value.incident!==undefined){keys(value.incident,['awareAt','deadlineHours','reportingRequired']);const x=value.incident;
  if(typeof x.awareAt!=='string'||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(x.awareAt)||!Number.isFinite(Date.parse(x.awareAt))||new Date(x.awareAt).toISOString().replace('.000','')!==x.awareAt||!Number.isInteger(x.deadlineHours)||x.deadlineHours<1||x.deadlineHours>8760||typeof x.reportingRequired!=='boolean')fail('Invalid declared incident trigger or deadline.');
  notification={awareAt:x.awareAt,declaredDeadlineHours:x.deadlineHours,deadlineAt:new Date(Date.parse(x.awareAt)+x.deadlineHours*3600000).toISOString(),reportingRequired:x.reportingRequired,applicability:'Declared scenario assumptions; privacy reviewer must confirm trigger, jurisdiction and notification duty.'};
 }
 return {schemaVersion:2,scenarioId:value.id,domain:value.domain,provenance:'Synthetic scenario; no client outcomes or verified evidence',domainReview,workspace,decisionLab,workspaceMetrics:metrics(workspace.records,input.asOf),decisionLabMetrics:derive(decisionLab),notification,decision:'Not authorized; human decision required'};
}
export function scenarioMemo(pack){return ['# '+pack.domainReview.assessment.deliverable,'',pack.provenance,'Domain: '+pack.domain,'Gate: '+pack.domainReview.readiness.gate,'Calculation: '+JSON.stringify(pack.domainReview.assessment.metric),'Recorded domain readiness: '+pack.domainReview.readiness.percent+'%','Recorded tested-control coverage: '+pack.workspaceMetrics.coverage+'%','Decision Lab high-priority signals: '+pack.decisionLabMetrics.high,'',...pack.domainReview.findings.map(f=>'- '+f.finding+'; '+f.nextAction),'',pack.notification?JSON.stringify(pack.notification):'No incident deadline declared.','',pack.decision].join('\n');}
