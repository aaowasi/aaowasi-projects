# Governance project workspace

Ten connected work samples in compliance, controls, third-party risk and AI governance, by Abdullah Al Owasi.

[Project workspace](https://aaowasi-projects.pages.dev/) · [Personal hub](https://aaowasi.pages.dev/) · [Portfolio](https://aaowasi.pages.dev/work/)

## Start here
1. Audit readiness: `projects/04-audit-readiness/manifest.json`
2. Vendor risk: `projects/03-tprm-ai-subprocessors/manifest.json`
3. AI governance: `projects/02-ai-governance/manifest.json`

## Run
```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 -m http.server 8000 --directory site
```

## Evidence model
The public assessment is explicitly synthetic. The private-use collector starts with empty evidence; missing evidence remains NOT_CONFIGURED. Public pages do not claim live client telemetry. Project manifests describe scope and expected outputs; they do not certify completion of every listed capability.

## Publishing
Cloudflare Pages: production branch `main`, build `python3 scripts/build_site.py`, output `site`. No server, paid API or database is needed for the public sites. Optional engine services run separately and are not deployed as static pages.

CI validates the site and Python engine. The manually triggered assurance workflow stores a review artifact; it does not publish raw evidence or create releases. OPA, optional MCP and container runtime validation require their own installed runtimes and have not been validated by the static-site checks.

See `docs/ARCHITECTURE.md` and `docs/OWNER_ACTIONS.md`.
