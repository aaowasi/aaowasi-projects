# P05

## 01 / Title & commercial priority

Executive risk — Tier 1.

## 02 / Domain & service scope

Enterprise risk, policy & advisory. Convert traceable assurance signals into appetite breaches, KRI trends, treatment decisions, and board-ready accountability.

The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

Use case: a risk committee needs a single register spanning AI, cloud suppliers, privacy and control exceptions, with explicit appetite and accountable risk treatment. The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId.

Focus fields for this module: likelihood, impact, treatment, reviewer, rationale, evidence. CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5.

JSON also carries provenance and editable assumptions. Limit: 250 records / 10 MB; unknown record fields are rejected.

Reference taxonomy: MITRE ATLAS. Import organizational records with their source and assessment date.

Snapshot asOf (YYYY-MM-DD) anchors expiry calculations. A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected.

Enter evaluation counts from completed model tests and link the supporting evidence. Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

All supplier signals feed the ERM register. AI approval and processor gaps add transparent points; unexpired current evidence with a passing control test earns a small policy credit.

Named acceptance requires a rationale; evidence or vendor edits immediately change the executive view.

## 05 / Working UI & decision layout

Board-priority table with inherent score, additive flags, evidence credit and final priority; inline treatment decision; scenario economics; exportable internal committee memo. Policy governance and internal-assurance scope appear as reviewer decisions, not automatic approvals.

Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

A keyboard-accessible 5×5 inherent-risk heatmap shows likelihood/impact counts; selecting a cell filters the register.

## 06 / Calculated outcome & ROI contract

High-priority exposure = count(priority ≥16) / all records × 100. Inherent = likelihood × impact; priority = clamp(inherent + flags − credit, 1, 25).

No annualized loss, risk probability or causal risk reduction is inferred. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero).

Enter review timings and delivery costs to calculate the business case. Validate the result against the next completed review cycle.

## 07 / Fast-track implementation, alternative & catch

Agree committee scope and appetite; calibrate ordinal likelihood/impact descriptions with owners; import one register; challenge high-priority items; approve treatment with rationale; review drift on a scheduled cadence in the approved review process. Alternative: export to the client’s risk register or ServiceNow workflow.

Catch: true risk aggregation, policy attestations, audit-committee approvals and financial loss models require governance and data beyond ordinal scores. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing.

Deploy those services before using the workspace for shared client operations.

## Sources

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
