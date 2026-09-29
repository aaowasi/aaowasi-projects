# P09

## 01 / Title & commercial priority

Processor governance — Tier 2.

## 02 / Domain & service scope

Privacy, processor contracts & transfers. Model controller, processor, subprocessor, processing, transfer, obligation, evidence, and change events as a reviewable relationship graph.

The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

Use case: a processor estate has missing DPAs and incomplete transfer-review references. Privacy operations must surface gaps without converting a checkbox into a legal finding.

The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: processor, dpa, region, transfer, reviewer, rationale.

CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions.

Limit: 250 records / 10 MB; unknown record fields are rejected. Reference taxonomy: MITRE ATLAS.

Import organizational records with their source and assessment date. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations.

A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Enter evaluation counts from completed model tests and link the supporting evidence.

Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

Processor flags filter a contract/transfer queue. Missing DPA or unresolved non-EEA/UK transfer review increases priority in ERM.

Vendor AI metadata still flows into AI governance; legal classification stays manual.

## 05 / Working UI & decision layout

Processor relationship table with DPA/transfer confirmations, region and gap indicators; reviewer rationale and internal decision memo. Region grouping prioritizes transfer reviews; confirm applicability with the privacy reviewer.

Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

## 06 / Calculated outcome & ROI contract

Processor gap rate = processor records missing DPA or required transfer review / processor records × 100; N/A if none. It measures metadata gaps, not GDPR compliance or transfer lawfulness.

Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero). Enter review timings and delivery costs to calculate the business case.

Validate the result against the next completed review cycle.

## 07 / Fast-track implementation, alternative & catch

Confirm controller/processor roles; map purposes and data categories; review Article 28 obligations and contracts; assess transfer mechanisms and onward processors with counsel; log regulatory change applicability; request missing evidence and obtain authorization. Alternative: maintain the legal records in an existing privacy platform and import minimized status metadata.

Catch: no agreement text is interpreted; fourth-party authorization trees, change-notice timers and legal transfer assessments remain a documented next phase. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing.

Deploy those services before using the workspace for shared client operations.

## Sources

- [GDPR, Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [EBA DORA register of information resources](https://www.eba.europa.eu/activities/direct-supervision-and-oversight/digital-operational-resilience-act/preparation-dora-application)
