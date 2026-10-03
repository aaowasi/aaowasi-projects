# Connected Governance Workspace

An inspectable connected GRC operating workspace for AI governance, third-party AI/LLM risk, audit readiness and continuous assurance.

[Live workspace](https://aaowasi-projects.pages.dev/workspace/) · [Recorded delivery evidence](https://aaowasi-projects.pages.dev/results/) · [Decision brief](https://aaowasi.pages.dev/contact/) · [Continuous GRC suite](https://aaowasi-projects.pages.dev/suite/)

## What this repository demonstrates

- **20 connected governance modules** across AI governance, third-party risk, audit readiness, privacy, technology risk and assurance.
- **13 GRC operating domains**, **16 shared record types** and **103 register/reporting views** in the continuous GRC suite.
- Browser-local editable records, explicit evidence states, transparent scoring and human review gates.
- Exportable decision memos, JSON round trips and CSV source records.
- Versioned manifests, schemas, tests, workflow validation and recorded delivery checks.

## Start with the live systems

### Connected risk workspace
Change AI inventory, SaaS/LLM vendor, privacy and evidence metadata once, then follow how the same facts affect risk priorities, drift/change signals, evidence coverage, review queues and decision outputs across ten modules.

[Open connected workspace →](https://aaowasi-projects.pages.dev/workspace/)

### Continuous GRC operating suite
Work across obligations, controls, suppliers, risks, evidence, incidents, privacy and AI governance in one operating surface.

[Open continuous GRC suite →](https://aaowasi-projects.pages.dev/suite/)

## Primary governance areas

| Area | Demonstrated mechanics |
|---|---|
| AI governance | AI inventory, NIST AI RMF / NIST AI 600-1 mapping, evaluation evidence, human oversight, release gates and post-deployment drift/change review |
| Third-party & AI vendor risk | SaaS / LLM intake, data-use and training/retention terms, subprocessors, assurance evidence, dependency risk and treatment decisions |
| Audit & continuous assurance | Drift detection, evidence freshness, control-test state, exceptions, remediation ownership and retest |
| Privacy & processor governance | DPA / processor relationships, transfer-review gaps, subprocessor changes and reviewer rationale |
| Executive technology risk | Likelihood/impact signals, appetite/tolerance views, KRIs and accountable treatment decisions |

## Run locally

```bash
npm run build
npm test
python3 -m unittest discover -s tests -v
python3 -m http.server 8000 --directory site
```

## Evidence boundaries

The public interfaces use synthetic scenario data and browser-local records so the mechanics can be inspected safely. They do not claim client telemetry, certification, an audit opinion or legal advice. Unsupported evidence remains visible as missing, stale, failed or manual-review state rather than being auto-approved.

## Framework focus

NIST AI RMF 1.0 · NIST AI 600-1 Generative AI Profile · ISO/IEC 42001:2023 · ISO/IEC 27001:2022 · SOC 2 · NIST CSF 2.0 · GDPR processor governance · EU AI Act transparency

## For a scoped review

If you have one AI use case, vendor set or assurance backlog, [send a decision brief](https://aaowasi.pages.dev/contact/) with the records in scope, evidence available and target date.

## Extended governance workflows

Twenty catalogue workflows connect specialist decisions with shared suite registers. Each project has a dedicated overview, focused section pages and onward links. Suite and specialist workspace datasets retain distinct schemas; transfer requires explicit reconciliation.
