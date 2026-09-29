# P01

## 01 / Title & commercial priority

Customer assurance — Tier 3.

## 02 / Domain & service scope

Customer assurance & claims. Turn customer claims into a traceable claim-control-evidence graph with freshness and exception states.

The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

Use case: a customer asks whether current evidence supports each contracted service. Sales needs an answer bounded by evidence state and reviewer ownership instead of a broad compliance claim.

The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: service, evidence, reviewer, rationale.

CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions.

Limit: 250 records / 10 MB; unknown record fields are rejected. Reference taxonomy: MITRE ATLAS.

Import organizational records with their source and assessment date. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations.

A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Enter evaluation counts from completed model tests and link the supporting evidence.

Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

Unexpired current evidence, a recorded passing control test and a named reviewer enables a supported draft. A change to stale/error immediately withdraws that support across customer assurance and questionnaires.

No external message is sent.

## 05 / Working UI & decision layout

Service-to-evidence register with supported-draft status and human reviewer, followed by an internal decision memo. Claims remain limited to the metadata, without certification or audit-opinion language.

Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

## 06 / Calculated outcome & ROI contract

Supported draft rate = records with unexpired current evidence, passing test and nonempty reviewer / all records × 100. This is drafting coverage, not customer trust improvement, revenue won or certification.

Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero). Enter review timings and delivery costs to calculate the business case.

Validate the result against the next completed review cycle.

## 07 / Fast-track implementation, alternative & catch

Agree customer scope; identify approved claim wording; locate control evidence; verify dates and ownership in the approved review process; record reviewer; redact confidential details; approve each external response in the client’s process. Alternative: publish approved artifacts in a client-managed trust center.

Catch: audience-specific access, redaction, contract interpretation and evidence freshness dates require production controls; the public portfolio contains no private artifacts. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing.

Deploy those services before using the workspace for shared client operations.

## Sources

- [AICPA SOC suite overview](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [GDPR, Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
