# P08 · Security questionnaires

## 01 / Title & commercial priority

Security questionnaires — Tier 3. This is the requested portfolio delivery priority, not independently verified market profitability. Independent, synthesized work sample; no client outcome or professional title is implied.

## 02 / Domain & service scope

Procurement questionnaires & response governance. Normalize customer questions, retrieve current evidence, draft bounded answers, and route unsupported claims for approval. The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

A fictional procurement team reviews control-specific procurement questions across six supplier services. An editable question and reusable bounded control-status draft can reduce retyping while refusing unsupported claims. The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: service, evidence, reviewer, rationale. CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions. Limit: 250 records / 10 MB; unknown record fields are rejected. Sample suppliers are invented. The MITRE subset is real public taxonomy, not client telemetry or benchmark results. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations. A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Evaluation counts are synthesized user inputs, not executed model tests. Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

The same current-evidence and reviewer gate drives P01 and P08. Changed evidence invalidates supported drafts immediately. Question text is editable. A deterministic control-status draft cites control ID, evidence reference, recorded outcome and validity dates; the reviewer must decide whether those facts answer the particular question. There is no semantic question answering or model retrieval.

## 05 / Working UI & decision layout

Questionnaire response table with editable procurement question context, per-service bounded draft, evidence state and reviewer. Unsupported rows show NO_CURRENT_EVIDENCE or missing-reviewer state rather than an invented answer. Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

## 06 / Calculated outcome & ROI contract

Supported answer coverage = supported drafts / all records × 100. Model economics must use measured minutes from a future timed pilot before any achieved productivity claim is made. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero). Default illustrative inputs: 90 manual minutes, 35 assisted minutes, 80 USD/hour, 1,200 USD setup. Six fictional records yield 5.5 hours, 440 USD gross, −760 USD net and −63.3% modeled ROI. No measured efficiency gain is claimed; replace inputs with timed pilot results before making a business case.

## 07 / Fast-track implementation, alternative & catch

Select a repeatable evidence-availability question; map each service to approved evidence; generate bounded drafts; check scope and validity manually; approve before sending; run a timed pilot and replace illustrative economics inputs. Alternative: import a client’s approved answer library into existing questionnaire software. Catch: bulk questionnaire document parsing, semantic retrieval, document parsing and external submission are not implemented here. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing. The public browser prototype implements none of those service guarantees.

## Primary references

- [AICPA SOC suite overview](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [GDPR, Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)

Sources checked 2026-09-24. Public mapped concepts only, not paid standards text.
