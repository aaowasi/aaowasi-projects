# P10 · Continuous assurance

## 01 / Title & commercial priority

Continuous assurance — Tier 3. This is the requested portfolio delivery priority, not independently verified market profitability. Independent, synthesized work sample; no client outcome or professional title is implied.

## 02 / Domain & service scope

Continuous assurance & remediation. Orchestrate collectors, evidence normalization, policy decisions, drift, finding lifecycle, SLA, retest, and immutable snapshots across the other nine modules. The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

A fictional control-evidence backlog mixes stale documents, missing evidence, a failed record and a collection error. Assurance operations need distinct owner actions and repeatable retest decisions. The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: evidence, owner, treatment, reviewer, rationale. CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions. Limit: 250 records / 10 MB; unknown record fields are rejected. Sample suppliers are invented. The MITRE subset is real public taxonomy, not client telemetry or benchmark results. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations. A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Evaluation counts are synthesized user inputs, not executed model tests. Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

The exception queue is a live filter of non-current evidence. Update a record to current after manual review and it leaves this queue, changes coverage and risk priority, and may enable a supported assurance draft.

## 05 / Working UI & decision layout

Exception table grouped by visible evidence state, owner and treatment; edit-and-recalculate workflow; memo export. Continuity and cloud gaps are treated as service context, not live health telemetry. Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes. Control IDs, evidence references, separate test outcomes and review/expiry dates support traceability; change the snapshot date to observe expiration. A state distribution reports missing/current/stale/failed/error counts.

## 06 / Calculated outcome & ROI contract

Backlog = records whose evidence state is not current. Closure scenario = prior backlog − current backlog, only if a separately retained baseline exists. The demo does not invent historical trend data or SLA attainment. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero). Default illustrative inputs: 90 manual minutes, 35 assisted minutes, 80 USD/hour, 1,200 USD setup. Six fictional records yield 5.5 hours, 440 USD gross, −760 USD net and −63.3% modeled ROI. No measured efficiency gain is claimed; replace inputs with timed pilot results before making a business case.

## 07 / Fast-track implementation, alternative & catch

Agree evidence freshness policy and remediation SLA; assign current backlog; troubleshoot collection errors separately; request evidence; execute authorized retests outside the browser; update status with rationale; export a review snapshot. Alternative: connect a client-managed ticketing workflow and scheduled collector service. Catch: no background jobs, immutable event timestamps, audit log or alert integration runs in the browser; those require authenticated services. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing. The public browser prototype implements none of those service guarantees.

## Primary references

- [NIST OSCAL assessment-results v1.1.3](https://pages.nist.gov/OSCAL-Reference/models/v1.1.3/assessment-results/)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)

Sources checked 2026-09-24. Public mapped concepts only, not paid standards text.
