# Owner actions and maintenance

## Cloudflare Pages: one-time verification
The connected browser could not pass Cloudflare's security verification. GitHub publishing can proceed, but the account's Pages settings must be verified separately if the Git push does not deploy.

1. Open your Cloudflare dashboard → Workers & Pages.
2. Open `aaowasi`. Confirm its Git repository is `aaowasi/aaowasi` and production branch is `main`.
3. Set Framework preset to None, build command to `python3 scripts/build_site.py`, build output directory to `site`, and root directory to the repository root (blank).
4. Apply the same settings to `aaowasi-projects`, using repository `aaowasi/aaowasi-projects`.
5. Retry the latest production deployment if no deployment starts after the Git push.
6. Check the production pages, `/work/` on the hub, and `/tools/vendor-review/` on the projects site.
7. Keep the Free plan. Neither public site requires a paid database, AI API or server.

Do not publish the repository root: it contains engine source and documents, while `site` is the intended public output.

## Add or update a project
1. Open `aaowasi-projects/content/projects.json` in GitHub and edit the relevant record.
2. Keep each `id` and URL-safe `slug` unique. Update title, summary, domain and type.
3. Add only destinations that exist: `liveUrl`, `caseStudyUrl`, `downloadUrl`, `codeUrl`. Missing actions are omitted automatically.
4. For a standalone app, set `liveUrl` to its precise public view. Include a back-to-hub link in that app.
5. For a manifest-backed case study, set `sourcePath` and provide the required manifest fields.
6. Commit. Cloudflare rebuilds the projects site if Git integration is enabled.
7. The hub's daily `Sync project catalogue` workflow copies the catalogue and regenerates its portfolio. To update immediately, run that workflow manually from Actions.
8. Branch protection may require a pull request or prevent the sync workflow's direct push. If enabled, use a PR-based sync instead of granting bypass access.

## Change home-page copy
Edit `aaowasi/templates/home.html`, not the generated `site/index.html`. Navigation and general static pages live under `site`. Shared styles are `site/assets/site.css`. The theme uses CSS variables for both modes.

## Evidence and client work
Public assessment data is a labeled synthetic sample. The manually triggered collector does not seed missing data with samples. Do not upload confidential client evidence to either public repository. Review artifacts before any public release. No claim of certification, audit opinion, paid engagement or operating history is implied by portfolio work.

## Career operating routine
- Lead applications with the most relevant one of the three featured artifacts.
- Track role, country eligibility, contract model, posting date, response, next action and evidence link.
- Prioritize compliance, controls assurance, audit readiness and TPRM scope.
- Agree daytime availability, deliverables, review cadence and exclusions before accepting work.
- Publish real outcomes only after obtaining client permission and removing confidential details.
- Add paid engagement evidence and references as they become available; change seniority claims only when supported.

## What stays manual
Client acceptance, evidence verification, risk decisions, employment eligibility and contractual commitments require accountable judgment. The public websites automate presentation and catalogue updates, not professional sign-off or job applications.

## LinkedIn consistency
Headline: Compliance Analyst | GRC & Security Compliance | Audit Readiness, SOC 2, ISO 27001 & TPRM | AI Governance

Use the personal hub as the primary website and feature audit readiness, vendor risk and AI governance. Keep education in progress and portfolio work identified accurately. Do not imply senior employment or paid clients that have not occurred.

## Recovery
Use Cloudflare's previous successful deployment for immediate rollback. Revert the corresponding Git commit to restore source. Keep the old v17/v18 sites available until the new sites are verified, then optionally redirect those legacy sites; this delivery does not delete the old sites.
