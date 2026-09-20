# Executive Loom scripts

## Script A: automation and continuous control monitoring

**Audience:** CISO, Head of GRC, Security Engineering Director  
**Target length:** 120 seconds

**0:00-0:15**  
"This repository turns control testing into a repeatable engineering workflow. I will show one collection run from source evidence to an immutable audit snapshot."

**0:15-0:35**  
Open `examples/client-context-saas-ai-eu.json`, then `config/control-tests.json`. "The run begins with organisational context. The framework selector proposes scope from jurisdiction, data, AI use, and contracts. Each control test has a source path, operator, owner, risk, due date, and remediation."

**0:35-0:58**  
Open `.github/workflows/ccm.yml`. "Every six hours, GitHub Actions starts read-only collection, runs deterministic tests, validates the repository, packages evidence, and creates a draft release. The workflow uploads every artifact before publishing, which protects the immutability boundary."

**0:58-1:20**  
Run the demo assessment. "The state model distinguishes pass, fail, not configured, error, not applicable, and manual review. Missing telemetry never becomes a pass. The demo intentionally fails Article 50 marking and vendor evidence coverage, so the pipeline preserves the report and then returns a failing status."

**1:20-1:42**  
Open the evidence manifest and report. "Each snapshot includes source provenance, timestamps, SHA-256 digests, control results, ownership, and remediation. Historical spreadsheets and PDFs move to a baseline release rather than cluttering the working branch."

**1:42-2:00**  
"The engineering result is continuous evidence, visible collection health, tested policy, and a defensible audit trail. The portfolio claim is bounded: this supports assurance work. It does not issue an audit opinion or legal conclusion."

Interview points:

- Explain why collector health and control effectiveness are separate states.
- Explain why the workflow preserves evidence before failing the job.
- Explain how private production evidence differs from the synthetic public demo.

## Script B: executive reporting and decisions

**Audience:** CISO, CRO, Head of Technology Risk, Board risk committee support  
**Target length:** 120 seconds

**0:00-0:15**  
"This view is a decision surface, not the system of record. Every number comes from the same control results and evidence references used by the assurance report."

**0:15-0:38**  
Open the portal in light and dark themes. "The first view explains the operating model and ten modules. It works without a JavaScript framework or external BI dependency, which keeps the public layer fast, inspectable, and inexpensive."

**0:38-1:02**  
Scroll to the six-state table. "I show pass and fail beside not configured, error, not applicable, and manual review. The effectiveness score uses only tested controls. Coverage and unresolved review remain visible, so a good percentage cannot conceal missing evidence."

**1:02-1:27**  
Open the Project 5 manifest. "The executive model consumes CCM findings, identity drift, vendor exposure, AI inventory, evidence age, and remediation status. Its outputs are appetite breaches, KRI movement, concentration risk, material exceptions, owners, and recorded decisions."

**1:27-1:48**  
Show an example finding in the Markdown report. "A board-level item must carry direction, threshold, exposure, owner, due date, treatment status, and the decision requested. The supporting control and evidence remain one click away."

**1:48-2:00**  
"This keeps executive reporting concise without breaking traceability. Public visuals use synthetic data. A production board view would remain private and role-restricted."

Interview points:

- Separate risk calculation from presentation.
- Describe score denominators and why exclusions must remain visible.
- Explain when native visualizations beat a public BI iframe.

## Script C: agentic AI governance and MCP

**Audience:** AI Governance Director, Security Engineering Director, TPRM leader  
**Target length:** 120 seconds

**0:00-0:15**  
"This demonstration connects AI governance, Article 50 transparency, shadow AI controls, and vendor triage through authorized, non-mutating MCP tools."

**0:15-0:38**  
Open `services/mcp-server/server.py`. "The server exposes narrow tools to list sanitized risks, retrieve a vendor, calculate a deterministic triage recommendation, scope frameworks, and assess controls. It does not let a model write risk acceptance or approve a vendor."

**0:38-1:00**  
Open `policies/opa/article50.rego`. "The Article 50 release gate checks direct-interaction disclosure and machine-readable marking for in-scope synthetic output. If the product invokes an exception or the legal classification is unclear, the workflow routes to manual review."

**1:00-1:23**  
Open the shadow AI project manifest. "The same evidence model ingests proxy, SaaS, or gateway events. It classifies the AI tool, detects sensitive egress, and returns allow, block, review, or exception states. Remote language models receive public data only unless an organization has approved a separate protected deployment."

**1:23-1:44**  
Run `evaluate_vendor` through an MCP client or show the returned JSON. "The score combines current residual risk, evidence age, critical findings, and fourth-party concentration. The output includes its inputs and sets `requires_human_approval` to true."

**1:44-2:00**  
"The point is bounded agency. Models can retrieve, classify, draft, and recommend. Identity, OPA authorization, deterministic checks, audit events, and human approval control the decision."

Interview points:

- Explain prompt injection as an authorization problem, not only a filtering problem.
- Explain why tool schemas, token scopes, and audit events matter more than model cleverness.
- Explain how Article 50 evidence becomes a release artifact instead of a policy statement.
