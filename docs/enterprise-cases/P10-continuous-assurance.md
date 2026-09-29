# P10

## 01 / Title & commercial priority

Continuous assurance — Tier 3.

## 02 / Domain & service scope

Continuous assurance & remediation. Orchestrate collectors, evidence normalization, policy decisions, drift, finding lifecycle, SLA, retest, and immutable snapshots across the other nine modules.

The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

Use case: a control-evidence backlog mixes stale documents, missing evidence, a failed record and a collection error. Assurance operations need distinct owner actions and repeatable retest decisions.

The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: evidence, owner, treatment, reviewer, rationale.

CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions.

Limit: 250 records / 10 MB; unknown record fields are rejected. Reference taxonomy: MITRE ATLAS.

Import organizational records with their source and assessment date. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations.

A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Enter evaluation counts from completed model tests and link the supporting evidence.

Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

The exception queue is a live filter of non-current evidence. Update a record to current after manual review and it leaves this queue, changes coverage and risk priority, and may enable a supported assurance draft.

## 05 / Working UI & decision layout

Exception table grouped by visible evidence state, owner and treatment; edit-and-recalculate workflow; memo export. Continuity and cloud gaps are treated as service context, not live health telemetry.

Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

Control IDs, evidence references, separate test outcomes and review/expiry dates support traceability; change the snapshot date to observe expiration. A state distribution reports missing/current/stale/failed/error counts.

## 06 / Calculated outcome & ROI contract

Backlog = records whose evidence state is not current. Closure scenario = prior backlog − current backlog, only if a separately retained baseline exists.

Retain dated baselines to calculate trends and SLA attainment. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero).

Enter review timings and delivery costs to calculate the business case. Validate the result against the next completed review cycle.

## 07 / Fast-track implementation, alternative & catch

Agree evidence freshness policy and remediation SLA; assign current backlog; troubleshoot collection errors separately; request evidence; execute authorized retests outside the browser; update status with rationale; export a review snapshot. Alternative: connect a client-managed ticketing workflow and scheduled collector service.

Catch: no background jobs, immutable event timestamps, audit log or alert integration runs in the browser; those require authenticated services. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing.

Deploy those services before using the workspace for shared client operations.

## Sources

- [NIST OSCAL assessment-results v1.1.3](https://pages.nist.gov/OSCAL-Reference/models/v1.1.3/assessment-results/)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
