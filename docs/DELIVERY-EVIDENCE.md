# Delivery evidence provenance

`content/verified-delivery.json` is a checked-in snapshot of actual public GitHub Actions run records, retrieved 2026-09-24T23:16:41.007Z. The published `/results/` page copies its timestamp, pinned commit SHAs, workflow names, status, conclusions and source URLs. `site/data/verified-delivery.json` is the downloadable generated copy.

The initial snapshot contains the hub Validate public site run and the projects Validate public site and Engine validation runs: three observed successful checks across two repositories. This is a bounded observation, not a complete run history, pass-rate estimate, production uptime or customer outcome. Each linked run exposes its actual workflow steps. The initial site runs predate adding JavaScript core tests to CI; they do not establish that those earlier runs executed the core tests.

Workflow elapsed is updatedAt minus createdAt, including queue and lifecycle time. It is not audit duration, isolated execution time or labor saved. The initial observed intervals are 12 seconds for the hub site, 13 seconds for the projects site and 11 seconds for the engine workflow. No client data or financial result is inferred.

To refresh explicitly, run `python3 scripts/refresh_delivery.py`. It requests public GitHub Actions records for the existing pinned commits and selected workflow names, selects the latest matching run by run ID, validates the observation, and writes only after all requests succeed. No private token or confidential data is needed. Public API rate limits and network failures can prevent refresh; the checked-in snapshot remains unchanged on request failure. To observe different commits, first update the pinned commits deliberately in the content file. Review the resulting source diff; run the build/tests and publish normally. No background refresh is introduced.

The build performs no network calls. It validates commit/run agreement, timezone-aware timestamps, nonnegative elapsed intervals and GitHub repository/run URLs before rendering escaped source values. The static page continues to describe its recorded commits after subsequent releases until explicitly refreshed.
