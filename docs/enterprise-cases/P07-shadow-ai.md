# P07 · Shadow AI governance

## 01 / Title & commercial priority

Shadow AI governance — Tier 1. This is the requested portfolio delivery priority, not independently verified market profitability. Independent, synthesized work sample; no client outcome or professional title is implied.

## 02 / Domain & service scope

Shadow AI, ethics & acceptable use. Discover AI usage, classify destinations and prompt data, enforce egress policy, and manage justified exceptions. The implemented browser slice and the production extension are distinguished below.

## 03 / Enterprise scenario, exact schema & sources

A fictional marketing tool is unapproved but processes public content; a support assistant is unapproved and handles personal data. Different data contexts need proportionate review without collecting employees’ prompts. The shared import contract is schemaVersion 1.0 with records containing exactly: id, name, owner, service, criticality, dataSensitivity, ai, approved, processor, region, dpa, transfer, disclosure, oversight, evidence, likelihood, impact, treatment, reviewer, rationale, parentVendorId, controlId, evidenceRef, testOutcome, evidenceReviewedAt, evidenceExpiresAt, question, aiEvalTotal, aiEvalFailed, techniqueId. Focus fields for this module: ai, approved, dataSensitivity, owner, treatment. CSV uses these field names as headers; booleans are true/false, likelihood and impact are integers 1–5. JSON also carries provenance and editable assumptions. Limit: 250 records / 10 MB; unknown record fields are rejected. Sample suppliers are invented. The MITRE subset is real public taxonomy, not client telemetry or benchmark results. Snapshot asOf (YYYY-MM-DD) anchors expiry calculations. A parentVendorId links a record to one upstream dependency; dangling links and cycles are rejected. Evaluation counts are synthesized user inputs, not executed model tests. Test outcome and evidence reference are distinct from evidence availability.

## 04 / Interconnected enterprise mechanics

Approved-tool status and classification generate allow/review/block candidates. The same unapproved AI flag opens an AI governance review and increases ERM priority. A block candidate is not enforced network traffic control.

## 05 / Working UI & decision layout

Destination inventory, data-classification selector, transparent candidate decision and owner editor. Only metadata is stored in memory; acceptable-use exceptions belong in reviewer rationale. Module navigation preserves one in-memory session; case-study navigation/reload does not. Export JSON to preserve changes.

## 06 / Calculated outcome & ROI contract

Review burden = unapproved AI destinations / AI destinations × 100. Sensitive block candidates = unapproved AI records with personal or sensitive classification. This is a record count, not measured incidents prevented. Shared model: hours = record count × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − setup cost (USD); ROI = net / setup cost (USD) × 100 (N/A when setup is zero). Default illustrative inputs: 90 manual minutes, 35 assisted minutes, 80 USD/hour, 1,200 USD setup. Six fictional records yield 5.5 hours, 440 USD gross, −760 USD net and −63.3% modeled ROI. No measured efficiency gain is claimed; replace inputs with timed pilot results before making a business case.

## 07 / Fast-track implementation, alternative & catch

Agree acceptable-use and ethical boundaries; conduct privacy and labor-law review before employee monitoring; inventory tool metadata; assign classifications and approvals; evaluate false positives with users; connect approved enforcement tooling only in a later controlled phase. Alternative: client-managed CASB/SSE discovery with privacy-preserving aggregation. Catch: no SIEM ingestion, endpoint sensor, prompt inspection or live blocking is implemented; exceptions require expiry and oversight in production. Production roadmap: authenticated identity and reviewer authorization, tenant-scoped storage, server-side validation, encryption, evidence access/retention controls, immutable event history, versioned integrations and independent security testing. The public browser prototype implements none of those service guarantees.

## Primary references

- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI 600-1 Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
- [GDPR, Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)

Sources checked 2026-09-24. Public mapped concepts only, not paid standards text.
