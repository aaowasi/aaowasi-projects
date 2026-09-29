# P08

## 01 / Title & commercial priority

Security questionnaires — Tier 3.

## 02 / Domain & service scope

Procurement questionnaires & response governance. Normalize customer questions, retrieve current evidence, draft bounded answers, and route unsupported claims for approval.

The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

Use case: a procurement team reviews control-specific procurement questions across six supplier services. An editable question and reusable bounded control-status draft can reduce retyping while refusing unsupported claims.

The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: service, evidence, reviewer, rationale.

CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions.

Limit: 250 records / 10 MB; unknown record fields are rejected. Reference taxonomy: MITRE ATLAS.

Import organizational records with their source and assessment date. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations.

A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Enter evaluation counts from completed model tests and link the supporting evidence.

Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

The same current-evidence and reviewer gate drives P01 and P08. Changed evidence invalidates supported drafts immediately.

Question text is editable. A deterministic control-status draft cites control ID, evidence reference, recorded outcome and validity dates; the reviewer must decide whether those facts answer the particular question.

There is no semantic question answering or model retrieval.

## 05 / Working UI & decision layout

Questionnaire response table with editable procurement question context, per-service bounded draft, evidence state and reviewer. Unsupported rows show NO_CURRENT_EVIDENCE or missing-reviewer state rather than an invented answer.

Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

## 06 / Calculated outcome & ROI contract

Supported answer coverage = supported drafts / all records × 100. Model economics must use measured minutes from a future timed pilot before any achieved productivity claim is made.

Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero). Enter review timings and delivery costs to calculate the business case.

Validate the result against the next completed review cycle.

## 07 / Fast-track implementation, alternative & catch

Select a repeatable evidence-availability question; map each service to approved evidence; generate bounded drafts; check scope and validity manually; approve before sending; run a timed pilot and replace illustrative economics inputs. Alternative: import a client’s approved answer library into existing questionnaire software.

Catch: bulk questionnaire document parsing, semantic retrieval, document parsing and external submission are not implemented here. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing.

Deploy those services before using the workspace for shared client operations.

## Sources

- [AICPA SOC suite overview](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [GDPR, Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
