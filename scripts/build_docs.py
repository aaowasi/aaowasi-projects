"""Generate client documentation and README architecture from actual routes and contracts."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json,re,hashlib
START='<!-- GENERATED-ARCHITECTURE:START -->';END='<!-- GENERATED-ARCHITECTURE:END -->'
class Elements(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.items=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ['a','button','summary','label']:self.stack.append([tag,a,[]])
 def handle_data(self,text):
  for x in self.stack:x[2].append(text)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:
    x=self.stack.pop(i);label=' '.join(' '.join(x[2]).split());
    if label:self.items.append((x[0],label,x[1]))
    break

def fingerprint(root):
 files=[]
 for folder in ['content','templates','scripts','functions','engine','services','policies','.github','site/assets','schemas']:
  for f in (root/folder).rglob('*'):
   if f.is_file() and f.suffix in ['.py','.js','.mjs','.css','.html','.json','.yml','.yaml','.sql','.rego'] and '__pycache__' not in str(f):files.append(f)
 if (root/'COMMERCIALIZATION.md').exists():files.append(root/'COMMERCIALIZATION.md')
 if (root/'GO_TO_MARKET.md').exists():files.append(root/'GO_TO_MARKET.md')
 # Static pages without source templates are also an authored interface contract.
 for route in ['decision-lab','tools/vendor-review','services','profile','contact','privacy','404.html']:
  f=root/'site'/route;f=f/'index.html' if f.is_dir() else f
  if f.exists() and not (root/'templates'/(route+'.html')).exists():files.append(f)
 h=hashlib.sha256()
 for f in sorted(set(files)):h.update(str(f.relative_to(root)).encode());h.update((re.sub(r'<head.*?</head>','',f.read_text(),flags=re.S) if f.suffix=='.html' and 'site/' in str(f.relative_to(root)) else f.read_text()).encode())
 return h.hexdigest(),sorted(str(f.relative_to(root)) for f in set(files))

ACTIONS={
'Open workflow':'Opens the domain-scoped workspace; the domain query selects its register and readiness checklist. No authorization decision is made by navigation.',
'Scope this workflow':'Opens the contact brief. Agree on system boundary, evidence inputs, acceptance criteria and review ownership before implementation.',
'Inspect source':'Opens the exact owned manifest in GitHub for capabilities, output contracts, framework anchors and dependency review.',
'View delivery evidence':'Opens recorded checks tied to an observation date and exact source commits. Historical checks do not certify current production systems.',
'Decision scope':'Expands the review purpose, domain capabilities and output contracts.',
'Framework anchors':'Expands applicable framework associations. Review applicability; an association is not an equivalent control or certification.',
'Upstream dependencies':'Expands links to source domains that supply inputs. Domain relationships may legitimately feed back; record-level vendor dependency cycles are rejected.',
'Downstream impacts':'Expands the dependent domains affected by this review; follow the linked project to inspect its scope.',
'Working review and evidence':'Explains domain record ownership and opens the scoped register.',
'Run readiness review':'Validates required scope and scoring fields and recalculates evidence validity, confirmed checks, qualitative risk and outstanding actions.',
'Load illustrative review':'Replaces only inspector form inputs with labeled example metadata and expired evidence to demonstrate a blocked gate. Does not change the shared register.',
'Reset review':'Clears the inspector form, sets today as reporting date and leaves all domain assertions unconfirmed.',
'Export review JSON':'Downloads the current findings, domain checks, framework anchors, dependencies and reviewer fields. Incomplete evidence remains visibly incomplete; it is not a suite-import file.',
'Structured review JSON':'Expands a text-only, dynamically recalculated JSON preview. Input strings are never injected as HTML.',
'Choose a perspective':'Scopes project cards, record metrics and table selection by domainSlug; selects the dedicated register and scrolls to the pipeline. All domains shows the full catalogue; unclassified legacy records remain visible there.',
'View':'Selects a register/reporting projection over the shared typed records. Changes the URL hash, not the underlying data.',
'Record type':'Chooses the entity schema for a new record. Existing-record type cannot be changed during editing.',
'Add record':'Opens the schema-based editor. Nothing is committed until Apply changes or Save & recalculate validates the record.',
'Apply changes':'Validates field types, counts, dates, reference types and dependency integrity; commits valid metadata and recomputes joined results.',
'Cancel':'Closes the editor without applying draft input.',
'Delete record':'Deletes only after confirmation. Incoming typed links must be removed first; rejected deletion leaves state unchanged.',
'Save on this device':'Explicitly saves suite JSON to this origin/browser localStorage. It is not shared across hosts, devices or users.',
'Restore saved data':'Validates and restores saved suite JSON; confirms replacement when current records exist.',
'Export JSON':'Downloads the complete typed suite including cross-domain links. Domain review exports use a different schema.',
'Import JSON':'Reads a local file, validates before replacing data, and rejects malformed fields, dangling links or cycles while preserving existing state.',
'Clear records':'Confirms removal of current suite state and its saved local copy. Export a backup before clearing.',
'Search records':'Filters the current register by case-insensitive record content without deleting any source records.',
'Sort':'Changes presentation order by ID, title, owner or review date.',
'Reporting date':'Sets the snapshot used for overdue and evidence-validity calculations; future evidence does not count as current coverage.',
'Load supplier / AI scenario':'Loads the labeled synthetic risk-core sample, confirms replacement when needed, and preserves a one-step undo checkpoint.',
'Start empty':'Clears Decision Lab in-memory records and resets assumptions; Undo last change can restore the checkpoint.',
'Undo last change':'Restores the most recent Decision Lab checkpoint, including records and scenario assumptions.',
'CSV template':'Downloads the exact Decision Lab CSV header contract with no customer data.',
'Apply date':'Validates the Decision Lab snapshot and recalculates evidence expiry.',
'Save & recalculate':'Validates the Decision Lab draft, commits it into its supplier/AI dataset and recalculates all specialist perspectives.',
'Remove record':'Rejects deletion with incoming vendor dependencies; otherwise checkpoints and removes the selected lab record.',
'Recalculate model':'Uses entered manual/assisted minutes, hourly cost and setup cost. Shows negative estimates and undefined ROI where setup cost is zero; it does not claim delivered savings.',
'Export decision memo':'Downloads scoring definitions, recorded decision fields and scenario assumptions for human review.',
'Export workspace JSON':'Downloads exact Decision Lab state for round-trip transfer; this is not the typed-suite schema.',
'Export records CSV':'Downloads Decision Lab source records with CSV formula-injection protection.',
'Import CSV / JSON':'Validates the Decision Lab file format, capacity and dependencies before replacing state.',
'Search work':'Filters the full project catalogue by readable content.',
'Domain':'Filters catalogue cards by the exact selected domain; All domains includes every project.',
'Format':'Filters catalogue cards by the available project type.',
'Reset':'Clears gallery search and filter values and restores the complete catalogue.',
'Back':'Uses browser history where available; falls back to the gallery.',
'Forward':'Uses browser forward history if available.',
'Prepare scope email':'Validates the contact form then opens an email draft. Delivery requires sending it in the email application.',
'Copy brief':'Copies the validated brief to the clipboard, with a recoverable error state if access fails.'}

def mechanism(tag,label,a):
 for key,value in ACTIONS.items():
  if label==key or label.startswith(key+' ') or label.startswith(key+' ↗'):return value
 if tag=='a':
  href=a.get('href','')
  if href.startswith('#'):return 'Moves to the matching page section; project details expand on hash navigation. No records are changed.'
  if '/work/' in href:return 'Opens the named dedicated project with review scope, readiness inputs, evidence needs and dependency links.'
  if 'github.com/aaowasi' in href:return 'Opens owned source or documentation in GitHub for technical inspection.'
  if '/workspace' in href:return 'Opens the typed operating workspace; query parameters choose a domain. Preserve current in-memory data through export before leaving.'
  return 'Navigates to the displayed destination. This action does not submit a form or alter a record.'
 if tag=='summary':return 'Expands or collapses this explanation without changing data. Keyboard Enter/Space activates it.'
 if tag=='label':return 'Accepts the explicitly labeled input; see the associated review or record schema below. Editing is local until the stated save action.'
 return 'Invokes the labeled page action; records remain unchanged unless a validated save, import or clear action completes.'

def generate(root):
 projects=json.loads((root/'content/projects.json').read_text());personal=not (root/'engine').exists();origin='https://aaowasi.pages.dev' if personal else 'https://aaowasi-projects.pages.dev';target='https://aaowasi-projects.pages.dev'
 configs=json.loads((root/'content/domain-reviews.json').read_text());catalog=json.loads((root/'content/suite-catalog.json').read_text());sig,files=fingerprint(root)
 pages=sorted((root/'site').rglob('*.html'));routes=['/'+str(p.parent.relative_to(root/'site')).replace('.','').strip('/')+'/' for p in pages if p.name=='index.html']
 diagram='''```mermaid
flowchart TD
 H["Personal hub"] --> G["Work catalogue"]
 H --> C["Contact brief"]
 G --> P["Dedicated domain projects"]
 P --> W["Typed operating workspace"]
 P --> R["Readiness inspector"]
 W --> E["Evidence and linked records"]
 E --> D["Human review and treatment"]
 D --> W
 G --> L["Supplier and AI Decision Lab"]
 L --> X["Memo, CSV and JSON exports"]
 R --> X
 H --> A["Native architecture and docs"]
 A --> P
 P --> V["Recorded delivery checks"]
```
'''
 dataflow='''```mermaid
flowchart TD
 S["Owned content and review contracts"] --> B["Python static build"]
 B --> U["Project pages and route index"]
 B --> J["Typed schemas and JSON definitions"]
 J --> F["Browser metadata validation"]
 F --> M["Evidence joins and risk calculations"]
 M --> Q["Reviewer decision and export"]
 Q --> F
 F --> O["Explicit device save"]
 B --> N["Generated DOCS and README map"]
 T["Source fingerprint and CI checks"] --> N
 K["Configured tenant identity"] --> API["Optional evaluation API"]
 API --> DB["Tenant quota and report storage"]
 API --> PR["Configured processing provider"]
```
'''
 lines=['# GRC suite: system guide and client demonstration manual','',f'Generated from {len(projects)} active domain projects, {len(catalog["entities"])} record types and {len(catalog["views"])} register/reporting views.','',f'Source contract SHA-256: `{sig}`','', '## System overview','', 'The portfolio is a static, owned-source website deployed from GitHub to Cloudflare Pages. The personal hub introduces the offer; the catalogue and project pages explain scope; the workspace stores typed governance metadata and recalculates joined views. No browser action silently approves risk, fetches an evidence URL, runs a cloud collector or sends confidential evidence.','',diagram,dataflow,'## Navigation and route contract','', '| Route | What it opens | Client purpose |','|---|---|---|']
 for route in routes:lines.append(f'| [{route}]({origin}{route}) | '+('Dedicated domain project and evidence-led readiness review' if route.startswith('/work/') and route!='/work/' else 'Named page, controls and destinations enumerated below')+' | Inspect scope, evidence and next action |')
 lines+=['','The personal hub and portfolio alias have separate browser origins. Device storage is origin-specific. Domain pages on the alias use the canonical project workspace for shared workflow destinations. The Decision Lab is a separate specialist supplier/AI model, not another copy of the typed suite. Its module tabs change in-memory projections; its project links open dedicated /work/ pages.','', '## State, validation and calculations','', '- Typed suite: `version: 1`, `records`, `updatedAt`; up to 5,000 records and 20 MB. Each record has an entity type, stable ID and optional domainSlug. Unknown fields, duplicate IDs, invalid typed references and vendor dependency cycles are rejected before committing.','- Inspector: one domain checklist per project, owner, boundary, reviewer, HTTPS evidence reference, validity date and domain-specific decision inputs. Readiness = confirmed checks / checklist length. Any missing scope, owner, reviewer, invalid evidence reference, expired evidence or unconfirmed check holds the gate. Even a complete gate only means ready for accountable review.','- Domain inspectors use coverage, declared tolerance, applicable deadline or recovery objective calculations. The separate typed suite high-risk threshold is ≥15. Decision Lab uses its documented separate policy: high ≥16 and moderate ≥9 after signal points and evidence credit. These are prioritization policies, not probabilities or interchangeable score scales.','- Typed control coverage joins scoped controls to all linked tests, including tests assigned to another domain. Only passing tests within the reporting-date validity period count. A passing test requires evidence URL, named reviewer and test date.','- Decision Lab: `schemaVersion: 1.0`; up to 250 records and 10 MB. A linked supplier/AI record carries evidence state, test result, reviewer, disclosure, oversight and processor metadata. Ten specialist views derive supplier, AI, evidence and questionnaire review signals. Import/export cannot silently interchange this model with the typed suite.','- In-memory edits are lost on page reload unless explicitly exported (or saved via the typed suite device-save button). Readiness review JSON is a report, not a suite import. Saving a form is an assertion, not evidence-content verification.','', '## Optional backend and integrations','', 'Cloudflare Pages Functions expose `/api/status`, `/api/login`, `/api/account`, `/api/evaluate`. With configured tenant identity, D1 and provider settings, the server validates identity and same-origin requests, validates input, atomically reserves tenant quota, enforces idempotency, calls the configured processing provider over HTTPS and stores a bounded report. Failed/unconfigured dependencies return an error or access-request state. Local browser counts never grant backend access. No billing, SSO or remote processing is claimed live without verified deployment configuration. Repository collectors, policies and OSCAL artifacts are integration building blocks and are not continuously running behind the public pages.','', '## Domain-by-domain operating and client guide','']
 for p,c in zip(projects,configs):
  lines +=[f'### {p["id"]}: {p["title"]}', '',f'**What and how:** [{p["title"]}]({target}/work/{p["slug"]}/) uses the `{p["entity"]}` typed register and its domain-specific readiness checklist. Inputs produce dated evidence gaps, ownership requests, a domain-specific assessment and an exportable version-2 JSON review.', '',f'**Why it exists:** {c["output"]}. Unowned or unsupported decisions create follow-up work and uncertain review boundaries.', '', '**Required assertions and evidence questions:**','']
  for check in c['checks']:lines.append('- '+check+'. Confirm the supporting artifact, owner and review date rather than relying on the checkbox alone.')
  lines +=['', '**Framework anchors:** '+ ' · '.join(c['frameworks'])+'. Applicability and control-level interpretation remain with the accountable specialist.', '', '**Upstream:** '+', '.join(c['upstream'])+'.', '**Downstream:** '+', '.join(c['downstream'])+'.','', '**B2B value:** Makes missing prerequisites and accountable next actions inspectable before release, procurement or assurance review. Agree a baseline for reviewer effort and overdue issues before claiming savings.','', '**Demo talking point:** “Here is the decision boundary for '+p['title'].lower()+'. I can change the recorded evidence date or remove one domain assertion and show exactly which prerequisite blocks review. The output preserves the responsible owner, evidence request and linked operating domains.”','']
 lines+=['## Every page control and action','', 'This inventory is generated from the shipped HTML. Repeated controls appear once per route. Dynamically rendered controls and form fields are explained after the inventory.','']
 for page in pages:
  parser=Elements();parser.feed(page.read_text());items=parser.items;route='/'+str(page.relative_to(root/'site')).replace('index.html','');seen=set();lines+=['### '+route,'','| Element | Operational logic | Business / demo use |','|---|---|---|']
  for tag,label,a in items:
   if (tag,label) in seen:continue
   seen.add((tag,label));dest=(' Destination: `'+a['href']+'`.') if a.get('href') else '';value=mechanism(tag,label,a)+dest
   lines.append('| '+label.replace('|','/').replace('\n',' ')+' | '+value.replace('|','/')+' | Show the input, destination or evidence state; describe the next accountable action rather than promising automatic compliance. |')
 lines+=['','## Dynamic controls, drawers and precise input contracts','', '- Domain perspective options are generated from content/projects.json; domain project counters derive from array length. Upstream/downstream cards resolve existing project slugs; no truncation is applied. All-domain mode renders the complete index.','- Edit [record ID] opens the actual typed record editor. Related-record links open the referenced record; the calculated column joins linked controls, tests and supplier dependencies. The preview never treats an arbitrary URL as verified evidence.','- Specialist Decision Lab tabs set the module query parameter, preserve the dataset, clear search/heat filters and recalculate the chosen projection. Browser Back restores the prior module. A 5×5 heatmap cell filters exact likelihood/impact and toggles off on a second click.','- Theme SVG button toggles the current origin between light and dark and persists an explicit user choice. New visitors start in light mode regardless of OS theme. Borderless appearance retains a visible keyboard focus outline.','- Project section links open matching details elements via hashchange and navigate to their exact IDs. Summary clicks open/close the accordion; upstream and downstream links navigate to separate dedicated projects.','- Inspector checklist options are domain-specific assertions listed in each module chapter. Changing any field recomputes findings and text-only JSON. Example/reset controls affect only this form. All-domain workspace hides the inspector until a domain is selected.','', '| Inspector input | Mechanism | Client question |','|---|---|---|','| Scope | Bounded nonempty system/service description | What exactly is included and excluded? |','| Owner | Named accountable party, not inferred from login | Who owns action and acceptance? |','| Evidence URL | HTTPS reference, no embedded credentials; content is not fetched | Where is authorized supporting evidence? |','| Valid until / reporting date | Valid calendar dates and expiry comparison | Does this evidence cover this review period? |','| Reviewer | Required human reviewer metadata | Who verifies it and makes the decision? |','| Likelihood / impact | Integer 1–5 qualitative assessment | What scoring policy and rationale did the client agree? |','', '## Typed record field dictionary','']
 for entity,fields in catalog['entities'].items():
  lines+=['### '+entity+' fields','','| Field | Accepted type / options | Operating purpose |','|---|---|---|']
  for field,kind in fields.items():lines.append('| '+field+' | '+str(kind).replace('|','/')+' | '+('Links to an existing '+kind[4:]+' record; checked before applying edits.' if isinstance(kind,str) and kind.startswith('ref:') else 'Records '+re.sub(r'([A-Z])',r' \1',field).lower()+' for scope, evidence or accountable review. Missing values remain unknown; they are not invented.')+' |')
 lines+=['', '## Client demo','', '<a id="client-demo"></a>','', '1. Start with the client’s decision: supplier approval, AI release, audit evidence or authorization boundary. Open that dedicated project.','2. Read the scope and framework anchors. Ask which jurisdiction, service population and reporting period apply.','3. Load the illustrative readiness review. Show expired evidence and two unconfirmed checks holding the gate. Change the evidence date and record the missing assertions to demonstrate the change, while explaining that evidence content still needs human verification.','4. Open the scoped typed register. Add a control/test or policy record, assign domain and owner, and inspect linked references. Show how evidence expiry changes coverage.','5. Use the supplier/AI Decision Lab only when that distinct model fits. Load its synthetic scenario, change a DPA/approval/evidence flag, switch specialist perspectives and show the resulting review queue.','6. Export the appropriate JSON or decision memo. Explain which schema it uses and how an owner can maintain the records.','7. Open recorded delivery checks for technical evidence, then agree a scope brief, client integration requirements, baseline measures and acceptance tests.','', '**Opening:** “This suite connects evidence, ownership and review decisions across the governance lifecycle. Let’s choose one real boundary and inspect the prerequisites that affect your next decision.”','', '**Hiring explanation:** “The source contracts, validation rules, domain gates and joined evidence calculations are inspectable. I can explain where the public browser tools stop and what identity, storage and integration controls a shared deployment needs.”','', '**Commercial scoping questions:** Which system/vendor population? Which evidence sources and dates? Who may approve exceptions? Which jurisdiction and baseline? Which records may be stored or processed? What turnaround, coverage and overdue-treatment measures will define acceptance?','', '## Maintenance and zero-stale-docs rule','', 'Run `python3 scripts/build_site.py` after any content, interface, workflow or source change. The build regenerates DOCS.md, the README route map, public docs page and synchronization fingerprint from source definitions and shipped controls. CI runs the build and contract check on pushes/PRs; generated changes must accompany implementation changes. The synchronization job commits README.md, DOCS.md, docs-sync.json and site outputs together. A source fingerprint mismatch or missing route fails the check. This is enforced at build/CI time, not a claim that arbitrary filesystem edits update docs without running the build.','', 'Adding a domain requires a unique project manifest, matrix entry, typed register mapping and domain-reviews checklist. The build uses these arrays for counts; tests verify every domain has its own checklist and resolves its upstream/downstream routes. Update authored explanations for changed semantics as well as generated inventories.','', '## Source file map','', '```text',*files,'```','', '## Licensing and terms','', 'Both repositories retain their existing AGPL-3.0 open-source LICENSE. TERMS_AND_CONDITIONS.md explains the public tool boundaries, acceptable use, data handling, service scope and distinction between code rights and advisory contracts. Required license and authorship notices are preserved. Referencing a framework does not imply affiliation or accreditation.','']
 lines+=['', '## Domain-specific deliverables and decision logic', '', 'Each project keeps shared evidence provenance and accountability while calculating its own business decision. There is no universal likelihood-times-impact gate. Numeric inputs are declared metadata, never measurements fetched from an API. Coverage rejects empty populations and completed counts above total; tolerance checks flag excess; deadline checks compare elapsed time with the supplied applicable deadline; recovery checks compare observed minutes with the approved objective. All attestations and domain checks require human verification. Thresholds are client inputs, not authoritative legal deadlines or framework pass marks.', '', '| Domain | Deliverable | Method | Decision inputs |', '|---|---|---|---|']
 for c in json.loads((root/'content/domain-reviews.json').read_text()):
  a=c.get('assessment')
  if a:lines.append('| '+c['title']+' | '+a['deliverable']+' | '+a['mode']+' | '+'; '.join(f['label'] for f in a['fields'])+' |')
 lines+=['', '**Interaction contract:** selecting a domain rebuilds its input form and resets the previous values. Editing inputs recalculates the named deliverable, findings and structured JSON. Run review performs the same calculation explicitly. Load illustrative review inserts synthetic, expired evidence and incomplete domain inputs; it cannot be mistaken for a client outcome. Reset removes the current metadata. Export decision memo validates the form and downloads a Markdown delivery report with the scope, calculation, evidence references, findings and dependency handoffs. It remains labelled unverified and not authorized. Export review JSON validates the form and downloads a version-2 JSON review with domain assessment, source references and upstream/downstream links; it does not submit or approve a report. Do not send sensitive documents to this public browser form.', '', '**Client demo:** choose the buyer’s decision, explain the input population and units, change an observed count or elapsed time, show the resulting exception and named deliverable, then identify the accountable reviewer. An AI evaluation threshold is specific to the declared sample and does not prove model safety. A supplier concentration ratio does not replace full due diligence. A privacy or incident deadline must be established for the actual trigger and jurisdiction.', '']
 lines+=['', '## Open core and commercial delivery', '', 'The AGPL-3.0 local core remains free to inspect, run and use under its license. Paid engagements cover bounded review, implementation, integration, training and scheduled support. Managed storage, SSO/roles, operated collectors and reporting are delivery scopes, not activated subscription features. The enterprise page request-scope action opens the personal contact brief; inspect-workspace opens the existing free core; organization-access opens the configured evaluation access route. No purchase or access entitlement is granted by these links. See https://aaowasi-projects.pages.dev/enterprise/ and the projects repository COMMERCIALIZATION.md for scope, proposed pricing, buyer demo guidance and release gates.', '']
 text='\n'.join(lines);(root/'DOCS.md').write_text(text)
 # Public guide uses native details sections; Markdown stays fully readable on GitHub.
 html=['<section class="section content"><p class="eyebrow">System and client guide</p><h1>Scope, evidence and decisions.</h1><p>Generated from the current route and data contracts.</p><p><a href="https://github.com/aaowasi/'+('aaowasi' if personal else 'aaowasi-projects')+'/blob/main/DOCS.md">Read the complete guide and diagrams on GitHub ↗</a></p></section>']
 for p,c in zip(projects,configs):html.append('<details class="project-detail"><summary>'+escape(p['id']+' · '+p['title'])+'</summary><div><p>'+escape(c['output'])+'</p><ul>'+''.join('<li>'+escape(x)+'</li>' for x in c['checks'])+'</ul><p>'+escape(' · '.join(c['frameworks']))+'</p><a href="'+target+'/work/'+p['slug']+'/">Open project and readiness review →</a></div></details>')
 html.append('<section class="section content" id="client-demo"><h2>Present the decision trail.</h2><ol><li>Choose the client’s system and review boundary.</li><li>Inspect framework applicability and prerequisites.</li><li>Change evidence validity and show which gate moves.</li><li>Identify the accountable reviewer and export the findings.</li><li>Agree integration scope and measurable acceptance criteria.</li></ol><a href="'+target+'/workspace/">Open operating workspace →</a></section>')
 template=(root/'templates/gallery.html').read_text();head=template.split('<main',1)[0];footer='<footer'+template.split('<footer',1)[1]
 dest=root/'site/docs/index.html';dest.parent.mkdir(exist_ok=True);dest.write_text(head+'<main id="main" class="wrap">'+''.join(html)+'</main>'+footer)
 block=START+'\n\n## Live architecture and route map\n\n'+f'{len(projects)} dedicated domain projects · {len(catalog["entities"])} typed records · {len(catalog["views"])} register/reporting views.\n\n'+diagram+dataflow+'\n[Complete operating and client guide](DOCS.md) · [Terms and conditions](TERMS_AND_CONDITIONS.md) · [License](LICENSE)\n\n### Domain project hierarchy\n\n'+ '\n'.join('- '+p['id']+' **'+p['title']+'** → [project]('+target+'/work/'+p['slug']+'/) → [workspace]('+target+'/workspace/?domain='+p['slug']+')' for p in projects)+'\n\n'+END
 readme=root/'README.md';s=readme.read_text();s=re.sub(r'\*\*20 connected governance (?:modules|workflows)\*\*','**'+str(len(projects))+' connected domain projects**',s);s=s.replace('**13 GRC operating domains**','**'+str(len(projects))+' GRC operating domains**').replace('**103 register/reporting views**','**'+str(len(catalog['views']))+' register/reporting views**')
 if START in s:s=s[:s.index(START)]+block+s[s.index(END)+len(END):]
 else:s+='\n\n'+block+'\n'
 readme.write_text(s);(root/'docs-sync.json').write_text(json.dumps({'sourceFingerprint':sig,'projectCount':len(projects),'routes':routes,'sources':files},indent=2)+'\n')
