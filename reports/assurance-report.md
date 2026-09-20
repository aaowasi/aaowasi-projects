# Enterprise Assurance Report

**Assessment:** AAO-DEMO-2026-001  
**Generated:** 2026-09-17T01:46:22.396075Z  
**Organization:** Example AI SaaS Ltd  
**Selected frameworks:** COSO-ERM, EU-AI-ACT, GDPR, ISO-22301, ISO-27001-2022, ISO-42001-2023, NIST-AI-RMF-1.0, NIST-CSF-2.0, SOC2  
**Effectiveness score:** 66.7%

## Executive summary

The engine recorded **6 pass**, **3 fail**, **0 not configured**, **0 error**, **0 not applicable**, and **1 manual review** results. The score excludes every non-tested state; exclusions remain visible.

## Domain and framework mapping

- **NIST-CSF-2.0 — NIST Cybersecurity Framework (2.0):** selected; The organization operates or is assessing a cybersecurity program
- **SOC2 — AICPA Trust Services Criteria / SOC 2 (current owner-approved criteria):** selected; The entity provides a service for customer data or operations, Customer assurance is in scope
- **ISO-27001-2022 — ISO/IEC 27001 (2022):** selected; An information security management system is in scope, A contractual ISO/IEC 27001 requirement exists
- **ISO-22301 — ISO 22301 (2019):** selected; Business continuity and resilience are in scope
- **NIST-AI-RMF-1.0 — NIST AI Risk Management Framework (1.0 (revision in progress)):** selected; AI is used in organizational processes, The organization provides an AI-enabled product or service
- **ISO-42001-2023 — ISO/IEC 42001 (2023):** selected; An AI management system is in scope
- **EU-AI-ACT — Regulation (EU) 2024/1689 (AI Act) (consolidated 2026-07-27):** selected; EU or EEA operations are declared, The AI system is placed on or used in the EU market
- **GDPR — Regulation (EU) 2016/679 (GDPR) (current consolidated text):** selected; EU personal data processing is declared, EU or EEA operations are declared
- **PCI-DSS-4.0.1 — PCI DSS (4.0.1):** not selected; No configured applicability signal matched
- **HIPAA-SECURITY — HIPAA Security Rule (current e-CFR):** not selected; No configured applicability signal matched
- **DORA — Regulation (EU) 2022/2554 (DORA) (current consolidated text):** not selected; EU or EEA operations are declared
- **NIS2 — Directive (EU) 2022/2555 (NIS2) (current):** not selected; EU or EEA operations are declared
- **COSO-ERM — COSO Enterprise Risk Management (2017):** selected; Enterprise risk management is in scope
- **CUSTOM — Organization-defined controls and contractual mandates (assessment supplied):** not selected; No configured applicability signal matched

## Control and gap matrix

| Control ID | Requirement / test | State | Risk | Evidence-based reason | Owner | Remediation |
| --- | --- | --- | --- | --- | --- | --- |
| IAM-001 | Administrative access requires MFA | PASS | HIGH | All observed administrative identities are protected by MFA | Identity and Access Management | Require phishing-resistant MFA for all administrative identities and retest coverage. |
| IAM-002 | Wildcard administrative grants are prohibited | PASS | CRITICAL | No wildcard administrative grant was detected | Cloud Security | Replace wildcard grants with least-privilege actions and scoped resources. |
| EVD-001 | Control evidence remains within the freshness SLA | PASS | MODERATE | Evidence is within the configured 30-day freshness SLA | GRC Operations | Refresh expired evidence and document an approved exception where automation is unavailable. |
| AI-001 | AI systems have an accountable owner | FAIL | HIGH | At least one AI system lacks an accountable owner | AI Governance | Assign a business owner and technical owner to every in-scope AI system. |
| AI-050-1 | Direct AI interaction disclosure | PASS | HIGH | The product exposes the configured AI-interaction disclosure | Product and Legal | Add context-appropriate disclosure before or at the first direct AI interaction. |
| AI-050-2 | Synthetic output marking is machine-readable and detectable | FAIL | HIGH | Machine-readable marking was not demonstrated | AI Platform | Implement interoperable provenance metadata or watermarking and retain detection-test evidence. |
| TPRM-001 | Critical vendors have current assurance evidence | FAIL | HIGH | At least one critical vendor lacks current assurance evidence | Third-Party Risk | Request current assurance evidence or approve a time-bound risk exception. |
| GDPR-28-1 | Processor agreement and subprocessor terms require legal review | MANUAL_REVIEW | HIGH | Contract terms, controller/processor roles, transfer mechanisms, and Article 28 sufficiency require qualified legal review. | Privacy and Legal | Review the executed DPA, subprocessor authorization mechanism, transfer basis, and flow-down terms. |
| DLP-001 | Sensitive prompt egress is blocked or approved | PASS | CRITICAL | No unapproved sensitive-data egress event was observed | Security Engineering | Block the destination, rotate exposed secrets where applicable, and route business exceptions for approval. |
| REM-001 | Critical findings meet remediation SLA | PASS | CRITICAL | No critical finding is overdue | Risk Owners | Escalate overdue critical findings, document the decision, and schedule evidence-backed retesting. |

## Audit and remediation roadmap

### Immediate / high priority

- **AI-001 (HIGH):** Assign a business owner and technical owner to every in-scope AI system. Owner: AI Governance. Target: 14 days.
- **AI-050-2 (HIGH):** Implement interoperable provenance metadata or watermarking and retain detection-test evidence. Owner: AI Platform. Target: 14 days.
- **TPRM-001 (HIGH):** Request current assurance evidence or approve a time-bound risk exception. Owner: Third-Party Risk. Target: 14 days.
- **GDPR-28-1 (HIGH):** Review the executed DPA, subprocessor authorization mechanism, transfer basis, and flow-down terms. Owner: Privacy and Legal. Target: 14 days.

### Follow-through

1. Confirm control ownership and risk acceptance authority.
2. Collect missing evidence through an approved connector or signed upload.
3. Remediate or approve a time-bound exception with rationale.
4. Retest the same deterministic procedure.
5. Publish the evidence bundle, manifest, report, and decision log as a release snapshot.

## Actionable evidence and operations request

- Assign a qualified reviewer for **GDPR-28-1 — Processor agreement and subprocessor terms require legal review** and record the decision basis.

## Limitations

- This reference engine scopes and tests configured controls; it does not issue certification, audit opinions, or legal advice.
- Legal applicability and subjective effectiveness judgments are routed to MANUAL_REVIEW.
