# Connected GRC ecosystem

Scope assets, data, suppliers and AI systems → establish obligations and authorization boundaries → link controls and owners → normalize evidence → review tests and treatments → record accountable decisions → recalculate and reopen on change.

## Runtime boundary

Public tools calculate locally on user interaction. Python collectors, OPA policies and evidence schemas are inspectable integration sources; production scheduling, credentials, tenant isolation and evidence retention require client deployment. No certification or automatic authorization is implied.

## Domain matrix

The following 22 enterprise and seven technical review areas are an extensible taxonomy, not a standard-defined or exhaustive list. Associations require applicability review and client-specific control testing.

| Domain | Framework anchors | Workflow | Output |
|---|---|---|---|
| Corporate governance & accountability | ISO/IEC 27001 clauses 4–6; NIST PM | [governance-program](https://aaowasi-projects.pages.dev/work/governance-program/) | Named owners, decisions and review dates |
| Enterprise risk & appetite | NIST RA; ISO/IEC 27001 clause 6 | [executive-risk](https://aaowasi-projects.pages.dev/work/executive-risk/) | Likelihood, impact, treatment and acceptance |
| Regulatory applicability & change | GDPR; EU AI Act; NIST PL | [regulatory-obligations](https://aaowasi-projects.pages.dev/work/regulatory-obligations/) | Jurisdiction, applicable requirement and effective date |
| Policy lifecycle | ISO/IEC 27001 clause 7; NIST PL | [policy-governance](https://aaowasi-projects.pages.dev/work/policy-governance/) | Version, ownership and attestation |
| Control implementation & ownership | NIST SP 800-53; ISO/IEC 27001 Annex A; SOC 2 TSC | [control-management](https://aaowasi-projects.pages.dev/work/control-management/) | Requirement → control → owner |
| Internal audit & independence | ISO/IEC 27001 clause 9; NIST CA | [internal-audit](https://aaowasi-projects.pages.dev/work/internal-audit/) | Plan, finding and corrective action |
| External audit & certification readiness | SOC 2 TSC; ISO/IEC 27001 clauses 9–10 | [audit-readiness](https://aaowasi-projects.pages.dev/work/audit-readiness/) | Reviewed tests and dated evidence |
| Continuous assurance & remediation | NIST CA-7; SOC 2 CC4 | [continuous-assurance](https://aaowasi-projects.pages.dev/work/continuous-assurance/) | Evidence expiry, failed tests and treatment |
| Supplier lifecycle & concentration | NIST SR; ISO/IEC 27001 Annex A | [vendor-risk](https://aaowasi-projects.pages.dev/work/vendor-risk/) | Tier, dependencies and exit conditions |
| Procurement & customer assurance | SOC 2 CC9; NIST SR | [customer-assurance](https://aaowasi-projects.pages.dev/work/customer-assurance/) | Requirements and evidence-backed answers |
| Privacy & individual rights | GDPR Articles 5, 12–22, 25, 35 | [privacy-lifecycle](https://aaowasi-projects.pages.dev/work/privacy-lifecycle/) | Purpose, retention and impact review |
| Processors & cross-border transfers | GDPR Articles 28, 30, 44–49 | [processor-governance](https://aaowasi-projects.pages.dev/work/processor-governance/) | DPA, subprocessors and transfer mechanism |
| Data classification & retention | GDPR Article 5; NIST MP, PT | [privacy-lifecycle](https://aaowasi-projects.pages.dev/work/privacy-lifecycle/) | Data owner, classification and deletion review |
| AI inventory & lifecycle authorization | NIST AI RMF; ISO/IEC 42001 | [ai-governance](https://aaowasi-projects.pages.dev/work/ai-governance/) | Inventory, evaluation and deployment decision |
| AI fairness, safety & oversight | NIST AI RMF MEASURE/MANAGE; ISO/IEC 42001 | [ai-governance](https://aaowasi-projects.pages.dev/work/ai-governance/) | Evaluation findings and human review gates |
| AI transparency & content provenance | EU AI Act Article 50 | [ai-transparency](https://aaowasi-projects.pages.dev/work/ai-transparency/) | Disclosure decision and evidence |
| Shadow AI & acceptable use | NIST AI RMF; ISO/IEC 27001 Annex A | [shadow-ai](https://aaowasi-projects.pages.dev/work/shadow-ai/) | Use-case intake and egress review |
| Continuity, recovery & crisis readiness | NIST CP; ISO/IEC 27001 Annex A | [resilience](https://aaowasi-projects.pages.dev/work/resilience/) | Critical services, recovery objectives and exercise evidence |
| Incident governance & reporting | NIST IR; GDPR Articles 33–34 | [remediation](https://aaowasi-projects.pages.dev/work/remediation/) | Incident owner, escalation and corrective action |
| Workforce, physical & organizational security | NIST AT, PS, PE; ISO/IEC 27001 Annex A | [governance-program](https://aaowasi-projects.pages.dev/work/governance-program/) | Control and review records; specialist assessment required |
| Financial, fraud & ethical conduct risk | NIST PM, RA; organization-specific legal obligations | [executive-risk](https://aaowasi-projects.pages.dev/work/executive-risk/) | Exposure and risk decisions; specialist assessment required |
| Sector, market & contractual obligations | Applicable sector rules; FedRAMP Rev5 when in scope | [regulatory-obligations](https://aaowasi-projects.pages.dev/work/regulatory-obligations/) | Applicability review; sector-specific controls require scoping |
| Security scope & authorization boundary | NIST RMF; NIST PL-2, CA-3 | [cyber-controls](https://aaowasi-projects.pages.dev/work/cyber-controls/) | Asset scope and system boundary; deployment architecture review |
| Identity, least privilege & segregation | NIST AC, IA; SOC 2 CC6 | [cyber-controls](https://aaowasi-projects.pages.dev/work/cyber-controls/) | IAM evidence and authorization policy source |
| Cloud configuration & change | NIST CM; SOC 2 CC8 | [cyber-controls](https://aaowasi-projects.pages.dev/work/cyber-controls/) | Configuration events and control decisions |
| Threat, vulnerability & supply-chain assurance | NIST RA-5, SI-2, SR | [cyber-controls](https://aaowasi-projects.pages.dev/work/cyber-controls/) | Alert normalization and remediation priorities |
| Logging, evidence integrity & provenance | NIST AU; SOC 2 CC7 | [continuous-assurance](https://aaowasi-projects.pages.dev/work/continuous-assurance/) | Source timestamps and evidence validation |
| Agent, tool & data authorization | NIST AC; NIST AI RMF | [ai-governance](https://aaowasi-projects.pages.dev/work/ai-governance/) | Agent/tool authorization policies and human escalation |
| Assessment, authorization & ongoing monitoring | NIST CA-2, CA-6, CA-7; FedRAMP Rev5 | [audit-readiness](https://aaowasi-projects.pages.dev/work/audit-readiness/) | Review packages; authorization remains with designated authority |

## Reference architecture

Reviewed native governance architecture as a reference for separation of policies, controls, metrics and audit artifacts. No code copied or integration affiliation implied.

## Deployment and customization

Run `npm run build` then `npm test`. Serve `site/` on Cloudflare Pages. To publish under aaowasi-portfolio.pages.dev, create that Pages project from this repository with output directory `site`; set the canonical base in scripts/seo.py to that host before generating. Only one canonical site should be indexed. Domain mappings: content/domain-matrix.json. Page layout: templates/architecture.html. Design tokens: site/assets/site.css.

## Value verification

Agree baseline reviewer effort, evidence turnaround, overdue treatments and tested-control coverage. Compare the same scoped population and reporting window after implementation; do not present modeled savings as measured outcomes.
