# Connected browser workspace

Open `/workspace/?module=ai-governance`. This is a static, browser-local portfolio application, not hosted enterprise SaaS. All module buttons use the same in-memory state. Query navigation and browser back/forward preserve it; page reload, case links and closing the tab discard it. Export JSON for an exact snapshot. One-step undo restores the state before record edits, imports, resets, clears and assumption changes.

## Data and boundaries

`site/assets/risk-core.mjs` owns version 1.0 normalization, strict record validation, CSV parsing/encoding, deterministic scoring and metric derivation. `site/assets/workspace.mjs` owns DOM rendering only, using textContent for user data. `site/data/workspace-schema.json` documents the contract; runtime additionally enforces unique IDs, valid calendar dates, acyclic dependency links, record relationships, failed evaluations <= total, explicit risk-acceptance rationale and complete current-evidence metadata. JSON top-level unknown keys are not retained. Record unknown fields are rejected. Max 250 records, 10 MB input, 300 characters per free-text field. No file contents or workspace records are transmitted or stored in localStorage; only the existing site theme preference uses localStorage.

Records join supplier/service metadata to one control, evidence reference, procurement question and optional AI evaluation summary. This is a deliberately normalized demonstration row, not a full relational enterprise inventory. One parent dependency per record supports direct dependant counts, not arbitrary multi-parent concentration modeling. Dates use the explicit snapshot `asOf`, avoiding hidden wall-clock changes. CSV imports use the default scenario date 2026-09-24 and default economic assumptions; use JSON to preserve those fields exactly. CSV export prefixes spreadsheet-formula candidates with an apostrophe; JSON preserves literal text for lossless round trips.

Current evidence is available and unexpired metadata; it is not automatically an effective control. Risk credit and supported response drafts additionally require a recorded passing test. Response drafts cite control/evidence/date provenance and do not automatically answer arbitrary legal or procurement questions. AI evaluation counts are synthesized planning data, not actual executed tests. A release-ready flag requires a nonempty failure-free evaluation set, tested oversight/disclosure, tool approval and unexpired passing evidence; legal applicability and final deployment approval remain manual.

## Primary-source provenance

`site/data/atlas-reference.json` contains five actual MITRE ATLAS technique identifiers/names extracted from the public dataset, content version 2026.09, format 6.0.0, retrieved 2026-09-24. Its source URL, SHA-256 and attribution are recorded. It supplies a real public reference taxonomy; all supplier records, evaluation counts and time/cost inputs are fictional. No empirical benchmark results are claimed. Project plans link verified primary sources: NIST AI RMF 1.0, NIST AI 600-1, CSF 2.0, OSCAL model references, OWASP LLM Top 10 2025, EBA DORA resources, GDPR, Commission AI transparency FAQ, AICPA SOC overview and ISO 42001 public overview. Concepts are mapped; licensed standard text is not reproduced. The custom schema is not an official DORA register, OSCAL assessment or compliance certification.

## Metric definitions

- Priority = clamp(likelihood × impact + signal points − evidence credit, 1, 25). Flags: unapproved AI +3; processor without DPA +3; processor outside EEA/UK without recorded transfer review +2. Unexpired current evidence with passing test earns 2 points credit. High ≥16; moderate ≥9. These are portfolio ordinal policy assumptions, not regulatory scores or probabilities.
- Evidence coverage = unexpired current records / all records. AI evaluation failure rate = total failed cases / total cases, never average of individual percentages. AI readiness uses AI records only; processor gaps use processor records only. Empty denominators display N/A.
- The heatmap uses inherent likelihood × impact, separately from adjusted priority. Every cell has a keyboard-accessible count and filter action.
- Workspace economics use all records, one review cycle, fixed scenario currency USD. Hours = records × (manual minutes − assisted minutes) / 60; gross = hours × hourly cost; net = gross − one-time setup; ROI = net / setup × 100, N/A for zero setup. Negative values are preserved. Defaults are illustrative and produce negative ROI for six records; they are not claimed delivered savings.

## Production path

Authentication, authorization, multi-tenant boundaries, durable storage, signed reviewer identity, tamper-evident event history, encrypted evidence custody, retention/deletion, secure file parsing, rate limits, integration secrets, jobs and operational monitoring require a separate service architecture. The browser does not implement SIEM ingestion, cloud collection, endpoint enforcement, actual model attacks, contract interpretation, external message sending or legal approval. Existing Python engine and legacy assessment routes remain available independently. See the seven-part plans in `docs/enterprise-cases/` for each bounded implementation slice, fast-track steps and alternative enterprise integration path.

## Verification

Run `npm run build && npm test`; core tests cover cross-module propagation, evaluation denominators, dated evidence, dependency cycles, CSV quoting, malicious spreadsheet prefixes, strict bounds, invalid inputs, acceptance gates, JSON round trips and negative/undefined scenario metrics. Browser smoke checks should exercise all module navigation, edit/save, import rejection, downloads, heatmap filtering, empty state and both themes at mobile and desktop widths.
