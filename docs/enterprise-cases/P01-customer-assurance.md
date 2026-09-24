# P01 · Customer assurance

## 01 / Title & commercial priority

Customer assurance — Tier 3. This is the requested portfolio delivery priority, not independently verified market profitability. Independent, synthesized work sample; no client outcome or professional title is implied.

## 02 / Domain & service scope

Customer assurance & claims. Turn customer claims into a traceable claim-control-evidence graph with freshness and exception states. The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

A fictional customer asks whether current evidence supports each contracted service. Sales needs an answer bounded by evidence state and reviewer ownership instead of a broad compliance claim. The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: service, evidence, reviewer, rationale. CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions. Limit: 250 records / 10 MB; unknown record fields are rejected. Sample suppliers are invented. The MITRE subset is real public taxonomy, not client telemetry or benchmark results. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations. A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Evaluation counts are synthesized user inputs, not executed model tests. Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

Unexpired current evidence, a recorded passing control test and a named reviewer enables a supported draft. A change to stale/error immediately withdraws that support across customer assurance and questionnaires. No external message is sent.

## 05 / Working UI & decision layout

Service-to-evidence register with supported-draft status and human reviewer, followed by an internal decision memo. Claims remain limited to the metadata, without certification or audit-opinion language. Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

## 06 / Calculated outcome & ROI contract

Supported draft rate = records with unexpired current evidence, passing test and nonempty reviewer / all records × 100. This is drafting coverage, not customer trust improvement, revenue won or certification. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero). Default illustrative inputs: 90 manual minutes, 35 assisted minutes, 80 USD/hour, 1,200 USD setup. Six fictional records yield 5.5 hours, 440 USD gross, −760 USD net and −63.3% modeled ROI. No measured efficiency gain is claimed; replace inputs with timed pilot results before making a business case.

## 07 / Fast-track implementation, alternative & catch

Agree customer scope; identify approved claim wording; locate control evidence; verify dates and ownership outside the demo; record reviewer; redact confidential details; approve each external response in the client’s process. Alternative: publish approved artifacts in a client-managed trust center. Catch: audience-specific access, redaction, contract interpretation and evidence freshness dates require production controls; the public portfolio contains no private artifacts. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing. The public browser prototype implements none of those service guarantees.

## Primary references

- [AICPA SOC suite overview](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [GDPR, Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)

Sources checked 2026-09-24. Public mapped concepts only, not paid standards text.
