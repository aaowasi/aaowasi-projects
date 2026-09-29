# Continuous GRC dashboard suite

Open https://aaowasi-projects.pages.dev/suite/. No workbook is required.

## Operating steps
1. Choose a view and record type. Add a record with a unique ID and title.
2. Create referenced records first. Controls link obligations and risks; tests link controls; risks link vendors, AI systems and decisions; supplier dependencies connect assets, processing, contracts and AI.
3. Apply changes to recalculate totals. Choose the reporting date for overdue and evidence coverage calculations.
4. Save on this device explicitly to retain data in this browser. Export JSON for backup or transfer. Restore/import replace the current dataset after confirmation.
5. Review linked records before deletion. Clear records removes the current dataset and device save.

## Calculation contract
- Risk: inherent likelihood × impact; residual likelihood × residual impact. Each input is an assessed integer 1–5. High inherent risk ≥15. No automatic effectiveness reduction.
- Control coverage: unique controls with at least one Pass test whose reviewer, HTTPS evidence link and test date are supplied, whose test date is no later than reporting date and expiry is on/after reporting date, divided by all controls. This checks entered metadata, not evidence content or authenticity.
- Overdue: reviewDate before reporting date, excluding Closed records.
- Supplier concentration: references to a vendor across assets, contracts, processing and AI divided by all vendor references across those types. This is record-count concentration, not spend or outage exposure.
- SLA/KPI: actual/value compared with target/threshold using At least or At most. Enter a consistent unit.
- Audit coverage: testedCount / populationSize. Selection methodology is entered text, not a statistical sampling engine.
- AI evaluation failure rate: evaluationFailed / evaluationTotal. These are entered evaluation results, not model tests run by this site.
- Policy attestations: attested / requiredAttestations. No automated notification or identity verification.
- Initiative budget remaining: budgetUSD − spentUSD.
- Maturity gap: targetLevel − currentLevel.
- Obligation rows count linked controls; control rows count linked tests and current passing tests. Issue age uses opening date through closure or reporting date. Evidence rows show expiry days. Asset rows flag pending patches on criticality 4–5. Decisions count assigned RACI roles; processing rows count five defined inventory fields. These are completeness and triage indicators, not legal compliance determinations.
- Zero denominators display — rather than an invented percentage.

## Data and limits
16 typed entity schemas, 5,000 records, 20 MB JSON. IDs are globally unique; references must exist and match type; risk/vendor dependency cycles are rejected. Text fields are rendered as text, not executable HTML. Import is atomic: rejected data does not replace current records.

The workspace processes data on the device. It has no authenticated accounts, tenant separation, server database, scheduled integrations, immutable audit log, email reminders or regulatory determinations. Device saving is not encrypted application storage. Use authorized data; protect the device and retain exported backups. Production multi-user deployment requires those controls and organizational validation.

## View coverage
The catalogue preserves all 95 requested labels and adds eight AI views. Labels are shared register perspectives, not 103 independent workflow engines. Entity-specific fields and calculated columns are shared consistently. Calendar views are date-sortable registers. Trend views expose dated records for review; historical charting is not implemented. Approval, attestation, policy and evidence states are recorded decisions, not enforced approval workflows.

| Domain | View | Shared entity |
|---|---|---|
| Compliance | Compliance Calendar Enterprise | obligation |
| Compliance | Compliance Obligations Register | obligation |
| Compliance | Compliance Status Dashboard | obligation |
| Compliance | Internal Compliance Checklist | obligation |
| Compliance | Regulatory Change Log | obligation |
| Compliance | Regulatory Crosswalk Matrix | obligation |
| Compliance | Compliance Remediation Tracker | issue |
| Compliance | Corrective Action Register | issue |
| Compliance | Non Compliance Incident Tracker | issue |
| Compliance | Compliance Testing Log | test |
| Control Management | Control Classification Matrix | control |
| Control Management | Control Inventory Template | control |
| Control Management | Control Ownership Matrix | control |
| Control Management | Control-to-Regulation Mapping Sheet | control |
| Control Management | Enterprise Control Library | control |
| Control Management | Risk-to-Control Mapping Sheet | control |
| Cybersecurity GRC | Asset Criticality Register | asset |
| Cybersecurity GRC | Patch Management Tracker | asset |
| Cybersecurity GRC | Vulnerability Prioritization Matrix | asset |
| Cybersecurity GRC | Cyber Risk Register | risk |
| Cybersecurity GRC | Threat Landscape Monitoring Log | risk |
| Cybersecurity GRC | Control Gap Assessment Template | control |
| Cybersecurity GRC | Security Maturity Assessment Model | assessment |
| Cybersecurity GRC | Security Maturity Assessment Model v2 | assessment |
| Cybersecurity GRC | Third-Party Risk Scoring Sheet | vendor |
| Cybersecurity GRC | Vendor Compliance Checklist | vendor |
| Dashboards & Analytics | Board Reporting Dashboard | all |
| Dashboards & Analytics | Compliance Dashboard | all |
| Dashboards & Analytics | Enterprise Risk Dashboard | all |
| Dashboards & Analytics | GRC Overview Dashboard | all |
| Dashboards & Analytics | Issue & Incident Dashboard | all |
| Dashboards & Analytics | KPI KRI Monitoring Panel | all |
| Dashboards & Analytics | Risk Exposure Summary Panel | all |
| Dashboards & Analytics | Risk Trend Analysis Sheet | all |
| Enterprise Risk Management | Emerging Risk Log | risk |
| Enterprise Risk Management | Enterprise Risk Register | risk |
| Enterprise Risk Management | Inherent vs Residual Risk Model | risk |
| Enterprise Risk Management | Residual Risk Calculator | risk |
| Enterprise Risk Management | Risk Categorization Matrix | risk |
| Enterprise Risk Management | Risk Dependency Mapping | risk |
| Enterprise Risk Management | Risk Heatmap Generator | risk |
| Enterprise Risk Management | Risk Impact Scoring Model | risk |
| Enterprise Risk Management | Risk Reporting Dashboard | risk |
| Enterprise Risk Management | Risk Velocity Tracker | risk |
| Enterprise Risk Management | Scenario Analysis Sheet | risk |
| Enterprise Risk Management | Strategic Risk Register | risk |
| Governance | Delegation of Authority Matrix | decision |
| Governance | Governance Decision Log | decision |
| Governance | Governance RACI Matrix | decision |
| Governance | Governance KPI Dashboard | metric |
| Governance | Governance Performance Scorecard | metric |
| Governance | Policy Approval Workflow | policy |
| Governance | Policy Attestation Tracker | policy |
| Governance | Policy Exception Register | policy |
| Governance | Policy Lifecycle Tracker | policy |
| Governance | Policy Repository Index | policy |
| Governance | Policy Review Calendar | policy |
| Incident & Issue Management | CAPA Log | issue |
| Incident & Issue Management | Enterprise Issue Log | issue |
| Incident & Issue Management | Incident Classification Matrix | issue |
| Incident & Issue Management | Issue Closure Tracker | issue |
| Incident & Issue Management | Issue Severity Matrix | issue |
| Incident & Issue Management | Contract Compliance Tracker | contract |
| Internal Audit | Audit KPI Dashboard | audit |
| Internal Audit | Audit Resource Allocation Sheet | audit |
| Internal Audit | Audit Universe Builder | audit |
| Internal Audit | Fieldwork Tracker | audit |
| Internal Audit | Risk-Based Audit Scoring Model | audit |
| Internal Audit | Sampling Methodology Sheet | audit |
| Internal Audit | Audit Findings Register | issue |
| Internal Audit | Issue Aging Dashboard | issue |
| Internal Audit | Management Action Plan Tracker | issue |
| Internal Audit | Control Testing Sheet | test |
| Internal Audit | Evidence Collection Log | test |
| KPI / KRI Management | Balanced Scorecard Template | metric |
| KPI / KRI Management | GRC-KPI Library | metric |
| KPI / KRI Management | KPI/KRI Mapping Sheet | metric |
| KPI / KRI Management | KRI Definition Register | metric |
| KPI / KRI Management | KRI Register | metric |
| KPI / KRI Management | Performance Monitoring Dashboard | metric |
| KPI / KRI Management | Continuous Improvement Tracker | initiative |
| Privacy | Data Breach Incident Log | issue |
| Privacy | Data Processing Inventory | processing |
| Privacy | Data Retention Schedule | processing |
| Privacy | Privacy Risk Register | risk |
| Program Management | GRC Capability Framework | assessment |
| Program Management | GRC Maturity Assessment Model | assessment |
| Program Management | GRC Initiative Tracker | initiative |
| Program Management | GRC Roadmap Planner | initiative |
| Third-Party Risk | Concentration Risk Analyzer | vendor |
| Third-Party Risk | Supplier Risk Scoring Matrix | vendor |
| Third-Party Risk | Third-Party Risk Register | vendor |
| Third-Party Risk | Vendor Risk Assessment Template | vendor |
| Third-Party Risk | Contract Compliance Tracker | contract |
| Third-Party Risk | Service-Level Monitoring Dashboard | contract |
| AI Governance | AI System Inventory | ai |
| AI Governance | AI Impact Assessment | ai |
| AI Governance | AI Lifecycle Review | ai |
| AI Governance | Human Oversight Register | ai |
| AI Governance | AI Evaluation Monitoring | ai |
| AI Governance | AI Vendor Governance | ai |
| AI Governance | AI Transparency Review | ai |
| AI Governance | AI Acceptable Use & Exceptions | policy |

## Framework sources
Public references, reviewed 28 September 2026: [NIST CSF 2.0](https://www.nist.gov/cyberframework), [NIST CPRT machine-readable catalog](https://csrc.nist.gov/projects/cprt/catalog), [NIST AI RMF 1.0](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/), [AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/). Framework references are separate from organizational records. The register starts empty; no fabricated company telemetry or client savings are included. The AI classification field is a review concern, not a legal determination.

## Build and deployment
From the projects repository root:
```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --test tests/browser/*.test.mjs
git add content templates scripts site tests docs README.md
git commit -m "Update continuous GRC suite"
git push origin main
```
Cloudflare Pages builds the connected main branch and publishes the site directory. The existing GitHub Actions checks validate the site and JavaScript core. Confirm the production /suite/ route after the deployment completes. Data recalculates when you edit or change the reporting date; no scheduled feeds or background organizational synchronization are configured.
