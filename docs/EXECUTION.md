# Execution, deployment, and debugging

## 1. Prepare the repository

```bash
unzip grc-ai-governance-engine-upgraded.zip
cd grc-ai-governance-engine
python -m venv .venv
. .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -v
python scripts/validate_repository.py
```

The test suite must pass before the first push. The demo assessment is designed to find control gaps and therefore returns exit code 1:

```bash
python -m engine.cli assess \
  examples/client-context-saas-ai-eu.json \
  examples/evidence/demo-signals.json
```

Review `reports/assurance-report.md`. Confirm that `FAIL`, `MANUAL_REVIEW`, and `NOT_CONFIGURED` appear as distinct states.

## 2. Create and secure GitHub

```bash
git init
git add .
git commit -m "Build adaptive GRC and AI assurance engine"
gh repo create grc-ai-governance-engine --public --source=. --remote=origin --push
```

Then configure the repository:

1. Require pull requests and status checks for `main`.
2. Enable Dependabot, secret scanning, and push protection where the account plan offers them.
3. Set Actions workflow permissions to read/write only because the CCM job creates releases.
4. Enable immutable releases before the first evidence release.
5. Keep all public data synthetic or approved and sanitized.

Do not add production cloud tokens to a public portfolio. If you test live collection, use a private fork and read-only, repository-scoped credentials.

## 3. Configure context and evidence

Copy and edit the examples:

```bash
cp examples/client-context-saas-ai-eu.json data/runtime/client-context.json
cp examples/evidence/demo-signals.json data/runtime/evidence-signals.json
```

Set exact jurisdictions, industries, data types, AI functions, contractual commitments, and scope boundaries. Run:

```bash
python -m engine.cli scope data/runtime/client-context.json
python -m engine.cli assess \
  data/runtime/client-context.json \
  data/runtime/evidence-signals.json
```

For an exported AWS IAM bundle:

```bash
python -m engine.cli collect aws-iam data/source/aws_iam.json \
  --output data/runtime/aws-iam-analysis.json
```

For GitHub alerts, set a read-only token with the minimum alert permissions, then run:

```bash
export GITHUB_REPOSITORY="OWNER/REPOSITORY"
export GITHUB_TOKEN="READ_ONLY_TOKEN"
python -m engine.cli collect github-alerts \
  --output data/runtime/github-alerts.json
```

## 4. Validate policy and MCP locally

```bash
docker compose up --build -d
curl -fsS http://127.0.0.1:8181/health
curl -fsS http://127.0.0.1:8181/v1/policies
docker compose logs mcp
docker compose down
```

Keep both services on loopback during local development. Before any remote exposure, add an identity-aware proxy, TLS, request limits, structured audit events, and OPA decisions for every tool.

## 5. Run continuous assurance

Open GitHub Actions and run `Policy and OSCAL Validation`. Then run `Continuous Assurance Snapshot` manually.

The snapshot workflow follows this order:

1. Collect evidence and run deterministic tests.
2. Preserve the assessment even when a control fails.
3. Validate JSON and repository structure.
4. Create a raw evidence archive and digest manifest.
5. Create a draft release.
6. Upload every asset.
7. Publish the release.
8. Mark the workflow failed if a control failed.

That final failure is intentional. It makes the risk visible without losing evidence.

## 6. Deploy the public portal

### Cloudflare Pages, recommended

1. In Cloudflare, open Workers & Pages and create a Pages project from the GitHub repository.
2. Select `main` as the production branch.
3. Leave the build command empty.
4. Set the output directory to `apps/portal`.
5. Deploy, then open the generated `pages.dev` URL.
6. Check that `apps/portal/data/control-status.json` loads and both themes work.

The static portal does not require a framework, Node build, database, or Worker. Deploy `workers/evidence-api` only if an API facade provides a real benefit.

### Vercel fallback

```bash
npx vercel --cwd apps/portal
npx vercel --cwd apps/portal --prod
```

Set Framework Preset to `Other`, Build Command to empty, and Output Directory to `.`. Do not configure serverless functions for the static reference portal.

### GitHub Pages fallback

Add a workflow that uploads `apps/portal` as the Pages artifact. Use a relative data URL, as the supplied `app.js` already does, so the site works below a repository path.

## 7. Optional BI embed

Use the native portal first. Add public BI only when its interaction is stronger than the local view.

1. Export a separate, sanitized dataset with no vendor names, findings text, control evidence, or personal data.
2. Publish it to the selected free BI service.
3. Enable its public embed setting.
4. Wrap the iframe in a responsive container with a fixed aspect ratio and a textual fallback link.
5. Test content security policy, third-party cookies, mobile interaction, keyboard access, and provider branding.

Grafana Cloud is the better fit for time-series control telemetry. Tableau Public fits exploratory public visuals. Power BI's free public sharing constraints should be verified against the current tenant and licensing before committing to it.

## 8. Migrate historical evidence

Create one baseline release instead of committing raw spreadsheets and PDFs to the main branch:

```bash
sha256sum legacy/* > legacy-sha256.txt
tar -czf legacy-baseline.tar.gz legacy legacy-sha256.txt
gh release create baseline-2026-09 \
  legacy-baseline.tar.gz legacy-sha256.txt \
  --title "Historical portfolio baseline" \
  --notes "Read-only source artifacts retained for migration traceability."
```

Confirm classification and publication approval before uploading any historical artifact. When source files contain client data, use a private repository or an approved evidence store.

## Device verification matrix

| Device class | Viewport | Required checks |
|---|---:|---|
| Small Android | 320 x 700 | No horizontal scroll, no clipped heading, readable project rows |
| Android baseline | 360 x 800 | 44px controls, theme persists, one-column order is logical |
| iPhone baseline | 390 x 844 | Safe viewport height, sticky header does not obscure anchors |
| Tablet portrait | 768 x 1024 | Grid transition is stable, line lengths remain readable |
| Laptop | 1366 x 768 | First viewport states the product and next action without clipping |
| Desktop | 1920 x 1080 | Type remains proportionate, content does not spread into unreadable lines |
| Ultrawide | 3440 x 1440 | Sections retain intentional alignment and do not stretch charts or prose |
| Zoom and text | 200% zoom | Navigation, state list, and project copy remain operable without two-axis scrolling |

Test Chrome, Firefox, Safari, and Edge. Use keyboard-only navigation, a screen reader landmark pass, `prefers-reduced-motion`, light and dark OS preferences, slow network throttling, and a forced data-fetch failure.

## Predictive failures and recovery

| Failure | Likely cause | Prevention and fix |
|---|---|---|
| Workflow cannot create a release | `contents: write` missing or repository rule blocks the bot | Keep workflow permission scoped to contents write, allow the Actions actor, rerun after rules are corrected |
| Immutable release rejects upload | Release was published before all assets arrived | Always create draft, upload, then publish. Create a new tag instead of editing history |
| CCM job is red after artifacts exist | A control failed by design | Open the report and remediate the finding. Do not change the workflow to hide the failure |
| GitHub alert collector returns 403 or 404 | Token lacks alert permissions, alerts are disabled, or the endpoint is unavailable for the repository | Use a fine-grained read-only token, enable the security feature, and keep the source state `ERROR` or `PARTIAL` |
| OPA container starts but policies fail | Rego v1 syntax or test regression | Run `opa check` and `opa test` against `policies/opa` before merging |
| MCP imports fail | Python SDK major version mismatch | Install `mcp>=2,<3` in a clean virtual environment and rebuild the container |
| MCP becomes publicly reachable | Port was bound to all interfaces or a proxy rule was added | Retain `127.0.0.1` binding locally. Require authentication and per-tool policy before remote access |
| Cloudflare shows 404 | Output directory is wrong | Set output to `apps/portal`, leave build blank, and redeploy |
| Status data never updates | Workflow output was not copied into the public data path | Publish only a sanitized summary to `apps/portal/data/control-status.json` through an approved PR or deployment job |
| Browser blocks API request | Origin mismatch or missing CORS header | Prefer same-origin static JSON. If using the Worker, set `ALLOWED_ORIGIN` to the exact scheme and hostname |
| Mobile page overflows | Long control IDs, unbounded grids, or animation transforms | Test at 320px, wrap identifiers, collapse to one column, and never move content outside the viewport |
| Public BI iframe is blank | Provider disables framing, URL is private, or CSP blocks it | Verify public sharing, frame policy, CSP `frame-src`, and a signed-out browser before publishing |
| Evidence archive leaks secrets | Raw payload was uploaded without classification or redaction | Stop the workflow before release, rotate exposed credentials, remove the release if mutable, and follow incident handling. Keep production evidence private |
| Framework score looks artificially high | Missing and review states were excluded without being shown | Keep the six-state table next to the score and report coverage separately |

## Maintenance with no downtime

- Evidence data: write a new timestamped snapshot, validate it, then publish. Never edit an old release.
- Controls and policies: change through a pull request with unit and Rego tests.
- Portal: publish sanitized JSON through the normal branch workflow. Static hosts swap deployments atomically.
- Framework registry: review quarterly and whenever a regulation, standard, contract, or product scope changes.
- Dependencies: review monthly, pin major versions, and test upgrades in a branch.
- Access: review tokens and service accounts quarterly. Remove unused credentials immediately.
- Exceptions: require an owner, reason, expiry date, compensating control, and retest date.
- Recovery: keep the last known-good static deployment and previous release artifacts. Roll the portal back without rewriting evidence history.

## Operations and permission action brief

Human action is required before the system can use live enterprise data:

| Action | Owner | Exact requirement |
|---|---|---|
| Create repository and deploy target | Repository owner | Create the GitHub repository and Cloudflare Pages project |
| Enable release immutability | Repository administrator | Turn on immutable releases before publishing audit snapshots |
| Supply data connections | System owner | Create read-only, least-privilege credentials in a private environment |
| Approve evidence publication | Data owner and security | Classify, sanitize, and authorize every artifact intended for a public release |
| Decide framework applicability | Legal, compliance, and audit | Review the selector output and record the approved scope |
| Approve risk and vendor decisions | Accountable risk owner | Review evidence and sign the final decision |
| Expose MCP remotely | Security engineering | Add authenticated gateway, authorization policy, logging, rate limits, and incident response |
| Rebuild the personal website | Portfolio owner | Upload the actual website Git repository so changes can be made and tested safely |
