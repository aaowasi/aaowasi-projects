import json

def generate(root):
 catalog=json.loads((root/'content/suite-catalog.json').read_text());configs=json.loads((root/'content/domain-reviews.json').read_text())
 entities=[]
 for name,fields in catalog['entities'].items():
  props={'type':{'const':name}}
  for key,kind in fields.items():
   if isinstance(kind,list):spec={'enum':kind+['',None]}
   elif kind in ['number','percent','score']:spec={'type':'number','minimum':1 if kind=='score' else 0};spec.update({'maximum':5 if kind=='score' else 100} if kind in ['score','percent'] else {})
   elif kind=='boolean':spec={'type':'boolean'}
   else:spec={'type':'string','maxLength':4000};spec.update({'format':'date'} if kind=='date' else {})
   if key=='id':spec={'type':'string','pattern':'^[A-Za-z0-9_-]{1,64}$'}
   props[key]={'anyOf':[spec,{'enum':['',None]}]} if key not in ['id','title'] else spec
  entities.append({'type':'object','required':['type','id','title'],'additionalProperties':False,'properties':props})
 workspace={'type':'object','required':['version','records','updatedAt'],'additionalProperties':False,'properties':{'version':{'const':1},'updatedAt':{'type':['string','null']},'records':{'type':'array','maxItems':5000,'items':{'oneOf':entities}}}}
 lab=json.loads((root/'site/data/workspace-schema.json').read_text());lab.pop('$schema',None)
 branches=[]
 for c in configs:
  fields={f['key']:({'type':'integer','minimum':f['min'],'maximum':f['max']} if f['type']=='number' else {'enum':f['options']}) for f in c['assessment']['fields']}
  branches.append({'properties':{'domain':{'const':c['slug']},'reviewInputs':{'properties':{'domainInputs':{'type':'object','required':list(fields),'additionalProperties':False,'properties':fields},'checks':{'type':'array','minItems':len(c['checks']),'maxItems':len(c['checks']),'items':{'type':'boolean'}}}}}})
 reviewprops={k:{'type':'string','maxLength':1500} for k in ['scope','owner','reviewer','evidenceURL','expires','asOf']};reviewprops.update(checks={'type':'array','items':{'type':'boolean'}},domainInputs={'type':'object'})
 schema={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'AAO executable domain scenario v1','type':'object','required':['scenarioVersion','id','domain','title','context','reviewInputs','workspace','decisionLab'],'additionalProperties':False,'properties':{'scenarioVersion':{'const':1},'id':{'type':'string','pattern':'^D[0-9]{2}-[123]$'},'domain':{'type':'string'},'title':{'type':'string','minLength':1,'maxLength':2000},'context':{'type':'string','minLength':1,'maxLength':2000},'reviewInputs':{'type':'object','required':list(reviewprops),'additionalProperties':False,'properties':reviewprops},'workspace':workspace,'decisionLab':lab,'incident':{'type':'object','required':['awareAt','deadlineHours','reportingRequired'],'additionalProperties':False,'properties':{'awareAt':{'type':'string','format':'date-time'},'deadlineHours':{'type':'integer','minimum':1,'maximum':8760},'reportingRequired':{'type':'boolean'}}}},'oneOf':branches}
 for path in ['schemas/scenario.schema.json','site/data/scenario-schema.json']:(root/path).write_text(json.dumps(schema,indent=2)+'\n')
 (root/'site/data/suite-schema.json').write_text(json.dumps(dict(workspace,**{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'AAO typed workspace v1'}),indent=2)+'\n')
