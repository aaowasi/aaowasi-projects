"""Build three executable synthetic delivery scenarios per registered domain."""
import json
from html import escape as e

def generate(root):
 configs=json.loads((root/'content/domain-reviews.json').read_text())
 catalog=json.loads((root/'content/suite-catalog.json').read_text())
 example=json.loads((root/'site/data/connected-scenario.json').read_text())
 cards=[];index=[]
 for n,c in enumerate(configs,1):
  for variant in range(1,4):
   passed=variant==2;mode=c['assessment']['mode']
   population,baseline=(10,10 if passed else 4 if variant==1 else 7) if mode=='coverage' else (0 if passed else 8 if variant==1 else 12,5)
   if mode=='deadline':population,baseline=(12 if passed else 80 if variant==1 else 96,72)
   if mode=='recovery':population,baseline=(45 if passed else 120 if variant==1 else 180,60)
   scenario_id=f'D{n:02d}-{variant}'
   contexts={1:'AI supplier onboarding: unverified subprocessors, missing DPIA review and unclear retention. '+c['assessment']['action'],2:'Annual cloud assurance preparation: scoped controls and recorded passing tests are complete. '+c['assessment']['acceptance'],3:'Unapproved generative AI handles customer PII across borders: map flows, establish transfer safeguards and assign corrective actions. '+c['assessment']['action']}
   review=dict(scope='Synthetic '+c['title']+' review',owner='Example '+c['entity']+' owner',reviewer='Example accountable reviewer',evidenceURL='https://example.com/evidence/'+scenario_id,expires='2027-01-31',asOf='2026-10-09',checks=[passed]*len(c['checks']),domainInputs=dict(population=population,baseline=baseline,approval='Confirmed' if passed else 'Pending review'))
   # Domain-owned register records and typed links are preserved, never flattened into the lab schema.
   obligation=dict(type='obligation',id=scenario_id+'-OB',title=c['title']+' applicability review',domainSlug='regulatory-obligations',framework='; '.join(c['frameworks']),requirement=c['checks'][0])
   control=dict(type='control',id=scenario_id+'-CT',title=c['assessment']['deliverable'],domainSlug=c['slug'],owner=review['owner'],obligationId=obligation['id'],effectiveness='Effective' if passed else 'Untested')
   test=dict(type='test',id=scenario_id+'-TS',title='Synthetic '+c['title']+' evidence test',domainSlug='audit-readiness',controlId=control['id'],result='Pass' if passed else 'Not tested',evidenceURL=review['evidenceURL'] if passed else '',reviewer=review['reviewer'] if passed else '',testedDate='2026-10-09' if passed else '',expiresDate='2027-01-31' if passed else '')
   # Use catalog's precise enumerations rather than guessed test labels.
   if not passed:test['result']=next(x for x in catalog['entities']['test']['result'] if x!='Pass')
   records=[obligation,control,test]
   vendor=dict(type='vendor',id=scenario_id+'-VD',title='Example AI supplier',domainSlug='vendor-risk',service='LLM support processing',usesAI=not passed,reviewOutcome='Approve' if passed else 'Pending',owner='Example supplier reviewer',notes='Synthetic: subprocessors reviewed' if passed else 'Synthetic: subprocessors unverified; retention unclear')
   records.append(vendor)
   entity=c['entity']
   detail={
    'policy':dict(version='1.0',approver='Example policy reviewer',attested=baseline if mode=='coverage' else 0,requiredAttestations=population if mode=='coverage' else 10),
    'audit':dict(scope=review['scope'],populationSize=population if mode=='coverage' else 10,testedCount=baseline if mode=='coverage' else 0,selectionMethod='Declared synthetic sample'),
    'processing':dict(purpose='LLM support / customer PII',lawfulBasis='Declared; requires privacy validation' if passed else '',dataCategories='Customer PII',retentionDays=30 if passed else 0,transferMechanism='Declared SCC review complete' if passed else '',vendorId=vendor['id']),
    'ai':dict(purpose='Customer support assistant',vendorId=vendor['id'],oversightOwner='Example AI reviewer',classification='Transparency review',evaluationTotal=20,evaluationFailed=0 if passed else 3,releaseDecision='Review' if passed else 'Hold',transparencyEvidence=review['evidenceURL'] if passed else ''),
    'metric':dict(definition=c['assessment']['fields'][0]['label'],value=population,threshold=baseline,direction='At most',unit='Declared domain unit',measuredDate=review['asOf']),
    'asset':dict(criticality=4,vendorId=vendor['id'],vulnerability='' if passed else 'Declared baseline exception',patchStatus='Applied' if passed else 'Pending'),
    'contract':dict(vendorId=vendor['id'],clause=c['checks'][0],slaActual=population,slaTarget=baseline,direction='At most',unit='Declared domain unit'),
    'decision':dict(accountable=review['owner'],responsible=review['reviewer'],consulted='Example privacy and security reviewers',informed='Example audit lead',rationale=c['assessment']['action']),
    'risk':dict(category=c['title'],likelihood=2 if passed else 4,impact=2 if passed else 4,treatment='Reduce',vendorId=vendor['id']),
    'assessment':dict(dimension=c['title'],currentLevel=5 if passed else 2,targetLevel=5,rationale=c['assessment']['action']),
    'initiative':dict(objective=c['assessment']['deliverable'],progressPercent=100 if passed else 40),
    'issue':dict(category=c['title'],severity='Low' if passed else 'High',status='Closed' if passed else 'Open',controlId=control['id'],openedDate='2026-10-09',correctiveAction=c['assessment']['action'])
   }.get(entity,{})
   if entity not in ['control','test','obligation','vendor']:
    records.append(dict(type=entity,id=scenario_id+'-DM',title=c['assessment']['deliverable']+' source record',domainSlug=c['slug'],owner=review['owner'],notes='Synthetic domain-specific inputs',**detail))
   if not passed:records.append(dict(type='issue',id=scenario_id+'-AC',title='Review prerequisites before release',domainSlug='remediation',owner=review['reviewer'],status='Open',controlId=control['id'],openedDate='2026-10-09',severity='High',correctiveAction=c['assessment']['action']))
   base=dict(id=scenario_id+'-AI',name='Example LLM support supplier' if variant==1 else 'Example cloud assurance service' if passed else 'Example shadow AI service',owner='Example service owner',service='Customer support' if variant==1 else 'Cloud assurance' if passed else 'Cross-border PII processing',criticality='high',dataSensitivity='personal',ai=not passed,approved=passed,processor=True,region='EEA' if passed else 'US',dpa=passed,transfer=passed,disclosure='tested' if passed else 'gap',oversight='tested' if passed else 'assigned',evidence='current' if passed else 'missing',likelihood=2 if passed else 4 if variant==1 else 3,impact=2 if passed else 4,treatment='mitigate',reviewer=review['reviewer'] if passed else '',rationale='Synthetic metadata only',parentVendorId='',controlId=control['id'],evidenceRef=review['evidenceURL'] if passed else '',testOutcome='pass' if passed else 'not-tested',evidenceReviewedAt='2026-10-09' if passed else '',evidenceExpiresAt='2027-01-31' if passed else '',question=c['checks'][0][:300],aiEvalTotal=0 if passed else 20,aiEvalFailed=0 if passed else 3,techniqueId='' if passed else 'AML.T0051')
   payload=dict(scenarioVersion=1,id=scenario_id,domain=c['slug'],title=['AI supplier onboarding','Recorded audit readiness','Cross-border AI incident'][variant-1]+' — '+c['title'],context=contexts[variant],reviewInputs=review,workspace=dict(version=1,records=records,updatedAt=None),decisionLab=dict(schemaVersion='1.0',asOf='2026-10-09',provenance='Synthetic scenario; evidence and passing tests are illustrative assertions',assumptions=dict(manualMinutes=0,assistedMinutes=0,hourlyCost=0,setupCost=0),records=[base]))
   if variant==3:payload['incident']=dict(awareAt='2026-10-09T09:00:00Z',deadlineHours=72,reportingRequired=True)
   path=f'/samples/{c["slug"]}/{variant}.json';dest=root/'site'/path.lstrip('/');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(payload,indent=2)+'\n')
   entry=dict(id=scenario_id,domain=c['slug'],title=payload['title'],url=path,context=contexts[variant],expectedGate='Ready for accountable review' if passed else 'Hold pending evidence and review',deliverable=c['assessment']['deliverable'],method=mode)
   index.append(entry)
  cards.append('<article class="card"><p class="eyebrow">'+f'D{n:02d}'+'</p><h2><a href="/work/'+c['slug']+'/">'+e(c['title'])+'</a></h2><p>'+e(c['assessment']['deliverable'])+'</p>'+''.join('<p><a download href="'+x['url']+'">Download '+e(x['title'].split(' — ')[0])+' JSON →</a></p>' for x in index[-3:])+'</article>')
 (root/'site/data/scenarios.json').write_text(json.dumps(index,indent=2)+'\n')
 shell=(root/'site/enterprise/index.html').read_text();start=shell.index('<main');end=shell.index('</main>')+len('</main>')
 body='<main id="main" class="wrap"><section class="hero"><p class="eyebrow">Executable delivery scenarios</p><h1>'+str(len(index))+' scenarios. '+str(len(configs))+' connected domains.</h1><p>Inspect the decision inputs, reproduce the calculation and export a review package. Synthetic data demonstrates behavior; it is not client evidence.</p><ol><li>Download one domain scenario below.</li><li>Import it into its domain review, <a href="/workspace/">Workspace</a> or <a href="/decision-lab/">Decision Lab</a>. A scenario contains separate version-1 typed records and schema-1.0 supplier records.</li><li>Inspect the domain-specific calculation, gate, source records and cross-domain links.</li><li>Export the version-2 scenario decision pack or Markdown memo. Native register exports remain separate.</li></ol><p><a href="/docs/#executable-scenarios">Calculation and demonstration guide →</a></p></section><section class="grid">'+''.join(cards)+'</section></main>'
 dest=root/'site/samples/index.html';dest.parent.mkdir(exist_ok=True);dest.write_text(shell[:start]+body+shell[end:])
