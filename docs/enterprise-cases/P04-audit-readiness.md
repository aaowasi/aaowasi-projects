# P04

## 01 / Title & commercial priority

Audit readiness — Tier 3.

## 02 / Domain & service scope

Control assurance, cloud & audit readiness. Execute repeatable test procedures and preserve observations, hashes, results, exceptions, and POA&M records in machine-readable form.

The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

Use case: a hosting control produces a collection error while payroll evidence is marked current. Internal assurance must separate evidence availability from whether cloud, access and continuity controls actually operate.

The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: evidence, owner, reviewer, service, rationale.

CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions.

Limit: 250 records / 10 MB; unknown record fields are rejected. Reference taxonomy: MITRE ATLAS.

Import organizational records with their source and assessment date. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations.

A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Enter evaluation counts from completed model tests and link the supporting evidence.

Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

Evidence states feed portfolio coverage, risk credit, assurance drafts and the P10 exception queue. Collection error never becomes fail or pass automatically; a reviewer must inspect and update the source record.

## 05 / Working UI & decision layout

Evidence register, explicit missing/current/stale/failed/error selector, assigned owner and reviewer. The custom workspace schema maps to assessment concepts; it is not OSCAL-conformant output.

Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

Control IDs, evidence references, separate test outcomes and review/expiry dates support traceability; change the snapshot date to observe expiration. A state distribution reports missing/current/stale/failed/error counts.

## 06 / Calculated outcome & ROI contract

Evidence coverage = current evidence records / all records × 100. Error count and failed count remain distinct.

This measures evidence status only, not control effectiveness, ISO certification or audit readiness as a percentage. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero).

Enter review timings and delivery costs to calculate the business case. Validate the result against the next completed review cycle.

## 07 / Fast-track implementation, alternative & catch

Define test scope and cloud/BCDR controls; identify evidence owner and collection period; sample access, backup restore and configuration evidence in the approved review process; distinguish collector failure from failed test; record observations; route remediation; retest with independent review. Alternative: use the existing Python assessment engine and client-approved collectors, then map outputs into a formal OSCAL assessment-results model.

Catch: this browser does not execute cloud checks or establish chain of custody for uploaded evidence. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing.

Deploy those services before using the workspace for shared client operations.

## Sources

- [NIST OSCAL assessment-results v1.1.3](https://pages.nist.gov/OSCAL-Reference/models/v1.1.3/assessment-results/)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [AICPA SOC suite overview](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)
