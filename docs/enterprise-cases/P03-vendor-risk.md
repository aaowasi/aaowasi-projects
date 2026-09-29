# P03

## 01 / Title & commercial priority

Third-party risk — Tier 2.

## 02 / Domain & service scope

Third-party lifecycle & concentration risk. Select proportionate vendor due diligence from service, data, access, AI, location, criticality, and dependency context.

The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

Use case: a service estate includes hosting, payroll, analytics and AI support vendors. Procurement needs a reusable intake that escalates critical and AI-enabled suppliers before contract approval.

The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: criticality, dataSensitivity, ai, processor, region, evidence.

CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions.

Limit: 250 records / 10 MB; unknown record fields are rejected. Reference taxonomy: MITRE ATLAS.

Import organizational records with their source and assessment date. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations.

A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Enter evaluation counts from completed model tests and link the supporting evidence.

Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

One vendor row becomes the common source for AI inventory, processor contract triage, ERM scoring and assurance evidence. Toggle Uses AI, save, then switch to P02 and P05 to observe propagation.

## 05 / Working UI & decision layout

Supplier intake table, criticality/data/AI flags, evidence-state editor and decision export. DORA register concepts inform service/relationship metadata, but the custom CSV is not an official DORA filing.

Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

The dependency graph is represented by parentVendorId edges; direct dependant counts expose shared-supplier concentration without inventing multi-hop percentages.

## 06 / Calculated outcome & ROI contract

Review coverage = records with current evidence / all suppliers × 100. Priority exposes ordinal assumptions; criticality is shown as context rather than silently assigned an unvalidated multiplier.

Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero). Enter review timings and delivery costs to calculate the business case.

Validate the result against the next completed review cycle.

## 07 / Fast-track implementation, alternative & catch

Set intake scope and critical-service criteria; load supplier metadata; flag AI and processing relationships; request evidence proportionate to service and data; assign reviewer; decide treatment; schedule periodic reassessment. Alternative: feed this documented schema into a client-managed TPRM platform.

Catch: multi-parent or multi-hop fourth-party concentration, contractual SLAs, exit planning and continuous vendor feeds need relationship and historical records not included in this minimum schema. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing.

Deploy those services before using the workspace for shared client operations.

## Sources

- [EBA DORA register of information resources](https://www.eba.europa.eu/activities/direct-supervision-and-oversight/digital-operational-resilience-act/preparation-dora-application)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
