# Governance project workspace

Ten connected work samples in compliance, controls, third-party risk and AI governance, by Abdullah Al Owasi.

[Project workspace](https://aaowasi-projects.pages.dev/) · [Personal hub](https://aaowasi.pages.dev/) · [Portfolio](https://aaowasi.pages.dev/work/)

## Interactive decision workspace

[Launch the ten-module workspace](https://aaowasi-projects.pages.dev/workspace/).

| Priority | Modules |
|---|---|
| AI governance and advisory | AI governance, executive risk, transparency, shadow AI |
| Supplier risk | Vendor risk, processor and dependency governance |
| Enterprise assurance | Audit readiness, continuous assurance, customer assurance, questionnaires |

Import CSV/JSON metadata, edit a supplier, inspect downstream AI and executive risk signals, review dated evidence, filter the risk heatmap and export a decision memo. One browser session connects all ten modules. Export JSON before leaving to preserve your work.

[Architecture and operating limits](docs/CONNECTED-WORKSPACE.md) · [Ten detailed case plans](docs/enterprise-cases/)

## Run

```bash
npm run build
npm test
python3 -m unittest discover -s tests -v
python3 -m http.server 8000 --directory site
```

## Evidence model
The public assessment is explicitly synthetic. The private-use collector starts with empty evidence; missing evidence remains NOT_CONFIGURED. Public pages do not claim live client telemetry. Project manifests describe scope and expected outputs; they do not certify completion of every listed capability.

## Publishing
Cloudflare Pages: production branch `main`, build `python3 scripts/build_site.py`, output `site`. No server, paid API or database is needed for the public sites. Optional engine services run separately and are not deployed as static pages.

CI validates the site and Python engine. The manually triggered assurance workflow stores a review artifact; it does not publish raw evidence or create releases. OPA, optional MCP and container runtime validation require their own installed runtimes and have not been validated by the static-site checks.

See `docs/ARCHITECTURE.md` and `docs/OWNER_ACTIONS.md`.

## Decision-oriented governance delivery

The portfolio connects ten disciplines through a versioned 30-field contract: supplier facts become AI reviews, processor gaps, executive priorities and evidence-backed response drafts. The workspace supports 250 records and 10 MB imports, with 13 JavaScript core tests and five existing Python engine tests.

Explore scoped AI governance, supplier/assurance sprints and recurring review deliverables through the [professional profile](https://aaowasi.pages.dev/profile/). Scenario economics remain modeled inputs; no client savings or production deployment is implied.
