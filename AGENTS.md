# Repository maintenance contract

Preserve truthful evidence states and human authorization boundaries. Never invent clients, results, endorsements or certification.

After changing a feature, interface, routing, data model, workflow, styling or integration: run `python3 scripts/build_site.py` and `python3 scripts/check_contract.py`; commit DOCS.md, README.md, docs-sync.json and generated site outputs with the implementation. Update authored explanations in scripts/build_docs.py and domain criteria in content/domain-reviews.json when behavior changes. The generated inventory is not a substitute for semantic review.

Run the site checks and relevant browser/core tests. All active domain projects must have unique slugs, valid dependencies and their own readiness checklist. Keep optional backend status truthful. Preserve the existing AGPL-3.0 LICENSE and legally required notices. Public project source links must resolve under aaowasi ownership.
