# P06

## 01 / Title & commercial priority

AI transparency — Tier 1.

## 02 / Domain & service scope

AI transparency & regulatory change. Operate product gates for AI-interaction disclosures, synthetic-output marking, deepfake disclosure, exceptions, and evidence retention.

The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

Use case: a product release combines an AI customer interaction and AI-generated marketing copy. Product and legal teams need an applicability review, disclosure test and accountable release decision.

The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: ai, disclosure, oversight, approved, evidence.

CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions.

Limit: 250 records / 10 MB; unknown record fields are rejected. Reference taxonomy: MITRE ATLAS.

Import organizational records with their source and assessment date. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations.

A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Enter evaluation counts from completed model tests and link the supporting evidence.

Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

AI systems from vendor intake populate transparency gates. A gap holds technical readiness; tested disclosure alone cannot clear a system without oversight, approval and evidence.

ERM remains connected to evidence and supplier flags.

## 05 / Working UI & decision layout

Disclosure-state table, technical gate indicator, source-record editor and a manual-review memo. The Commission Article 50 FAQ is a dated review input; no universal applicability or deadline is automatically assigned.

Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

## 06 / Calculated outcome & ROI contract

Technical readiness rate = technically ready AI records / AI records × 100. Readiness requires tool approval, tested disclosure and oversight, unexpired current evidence, a passing control test and a nonempty evaluation set with zero failures and is not an Article 50 compliance percentage.

Missing AI denominator returns N/A. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero).

Enter review timings and delivery costs to calculate the business case. Validate the result against the next completed review cycle.

## 07 / Fast-track implementation, alternative & catch

Confirm provider/deployer role and scope with counsel; monitor the official FAQ for regulatory changes; document applicability and exceptions; test notice accessibility and any required marking; retain test references; authorize release manually. Alternative: embed a transparency checklist in the existing release-management system.

Catch: actual UI disclosures, machine-readable marking interoperability and applicability analysis must be tested on the real product; they are not performed by this page. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing.

Deploy those services before using the workspace for shared client operations.

## Sources

- [European Commission Article 50 transparency FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)
- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
- [ISO/IEC 42001 public overview](https://www.iso.org/standard/42001)
