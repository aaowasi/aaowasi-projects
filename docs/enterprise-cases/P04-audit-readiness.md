# P04 · Audit readiness

## 01 / Title & commercial priority

Audit readiness — Tier 3. This is the requested portfolio delivery priority, not independently verified market profitability. Independent, synthesized work sample; no client outcome or professional title is implied.

## 02 / Domain & service scope

Control assurance, cloud & audit readiness. Execute repeatable test procedures and preserve observations, hashes, results, exceptions, and POA&M records in machine-readable form. The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

A fictional hosting control produces a collection error while payroll evidence is marked current. Internal assurance must separate evidence availability from whether cloud, access and continuity controls actually operate. The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: evidence, owner, reviewer, service, rationale. CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions. Limit: 250 records / 10 MB; unknown record fields are rejected. Sample suppliers are invented. The MITRE subset is real public taxonomy, not client telemetry or benchmark results. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations. A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Evaluation counts are synthesized user inputs, not executed model tests. Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

Evidence states feed portfolio coverage, risk credit, assurance drafts and the P10 exception queue. Collection error never becomes fail or pass automatically; a reviewer must inspect and update the source record.

## 05 / Working UI & decision layout

Evidence register, explicit missing/current/stale/failed/error selector, assigned owner and reviewer. The custom workspace schema maps to assessment concepts; it is not OSCAL-conformant output. Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes. Control IDs, evidence references, separate test outcomes and review/expiry dates support traceability; change the snapshot date to observe expiration. A state distribution reports missing/current/stale/failed/error counts.

## 06 / Calculated outcome & ROI contract

Evidence coverage = current evidence records / all records × 100. Error count and failed count remain distinct. This measures evidence status only, not control effectiveness, ISO certification or audit readiness as a percentage. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero). Default illustrative inputs: 90 manual minutes, 35 assisted minutes, 80 USD/hour, 1,200 USD setup. Six fictional records yield 5.5 hours, 440 USD gross, −760 USD net and −63.3% modeled ROI. No measured efficiency gain is claimed; replace inputs with timed pilot results before making a business case.

## 07 / Fast-track implementation, alternative & catch

Define test scope and cloud/BCDR controls; identify evidence owner and collection period; sample access, backup restore and configuration evidence outside the demo; distinguish collector failure from failed test; record observations; route remediation; retest with independent review. Alternative: use the existing Python assessment engine and client-approved collectors, then map outputs into a formal OSCAL assessment-results model. Catch: this browser does not execute cloud checks or establish chain of custody for uploaded evidence. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing. The public browser prototype implements none of those service guarantees.

## Primary references

- [NIST OSCAL assessment-results v1.1.3](https://pages.nist.gov/OSCAL-Reference/models/v1.1.3/assessment-results/)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [AICPA SOC suite overview](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)

Sources checked 2026-09-24. Public mapped concepts only, not paid standards text.
