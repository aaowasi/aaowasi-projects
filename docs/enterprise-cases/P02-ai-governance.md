# P02

## 01 / Title & commercial priority

AI governance — Tier 1.

## 02 / Domain & service scope

AI lifecycle & evaluation governance. Govern AI use cases from discovery and classification through evaluation, deployment authorization, monitoring, and retirement.

The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

Use case: a customer-support AI supplier handles personal data while an analytics assistant has approved oversight. The AI register must establish purpose, owner, provenance and evaluation responsibilities before model deployment.

The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: ai, approved, oversight, disclosure, evidence, dataSensitivity.

CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions.

Limit: 250 records / 10 MB; unknown record fields are rejected. Reference taxonomy: MITRE ATLAS.

Import organizational records with their source and assessment date. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations.

A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Enter evaluation counts from completed model tests and link the supporting evidence.

Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

AI-flagged supplier records become the AI inventory. Missing approval, tested oversight or tested disclosure creates a review; changing evidence also recalculates executive priority.

Attach completed evaluation results to support the release decision.

## 05 / Working UI & decision layout

AI inventory table → oversight and disclosure editor → linked evidence → release-review memo. Use the public MITRE ATLAS reference AML.T0051 (prompt injection), AML.T0054 (jailbreak) and AML.T0020 (poisoning) as evaluation-planning categories; link each evaluation result to its test report.

Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

The register exposes technique ID, total/failed evaluation counts and failure rate = failed / total × 100, with N/A for zero cases. Evaluation rates calculate from imported test totals and failures.

## 06 / Calculated outcome & ROI contract

AI review rate = unresolved AI reviews / AI-flagged records × 100; N/A with no AI records. Technical gate rate = AI records with approved tool + tested disclosure + tested oversight + unexpired current evidence + passing control test + at least one evaluation case with zero recorded failures / AI records.

Neither is a legal clearance. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero).

Enter review timings and delivery costs to calculate the business case. Validate the result against the next completed review cycle.

## 07 / Fast-track implementation, alternative & catch

Inventory one supplier and its model purpose; assign lifecycle owner; define task-specific safety, accuracy and red-team evaluation acceptance criteria; run controlled offline tests in a separately approved environment; record evidence and seek independent deployment authorization. Alternative: use an existing model registry and client-managed AI governance platform.

Catch: model/version-specific evaluation results, bias/fairness assessment and post-deployment monitoring need real measurements; attach model-version-specific test reports. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing.

Deploy those services before using the workspace for shared client operations.

## Sources

- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI 600-1 Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [MITRE ATLAS public techniques, 2026.09](https://github.com/aaowasi/aaowasi-projects/blob/main/DOCS.md
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
- [ISO/IEC 42001 public overview](https://www.iso.org/standard/42001)
