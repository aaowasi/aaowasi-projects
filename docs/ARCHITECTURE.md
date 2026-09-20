# Ecosystem architecture

## Delivery choice
A static HTML/CSS/JavaScript public layer, built from JSON with standard-library Python. This avoids paid APIs, client-side framework hydration and CMS administration. The engine stays in the projects repository, outside the published `site` directory. A future app can use any framework and be added with its own URL.

## Component hierarchy
- Site shell: metadata, skip link, identity, navigation, theme preference, footer.
- Hub: editorial introduction, featured work, professional narrative, services and contact.
- Portfolio: search, domain filter, format filter, project collection, empty state.
- Project: return-to-hub navigation, problem, method, output contract and review boundaries.
- Tools: local vendor triage; sample assessment table and JSON export.
- Contact: validated brief composer opening the visitor's email client.

## Routes
| Site | Route | Purpose |
|---|---|---|
| Hub | `/` | Brand and selected work |
| Hub | `/work/` | Full catalogue |
| Hub | `/profile/` | Printable professional profile |
| Hub | `/contact/` | Email brief composer |
| Projects | `/` | Project directory |
| Projects | `/work/<slug>/` | Deep-linked case study |
| Projects | `/tools/vendor-review/` | Local triage tool |
| Projects | `/assurance/` | Synthetic assessment results |
| Both | `/privacy/`, `/404.html` | Privacy and recovery |

## Data contract
`content/projects.json` is the source catalogue. Schema: `schemas/project.schema.json`. Required: id, slug, title, type, domain, summary. Optional: liveUrl, caseStudyUrl, downloadUrl, codeUrl, featured, featuredOrder, evidenceBasis, frameworks. Formats and domains are open strings, so new formats need no UI code changes. HTTPS and local-relative URLs only. Conditional actions omit missing destinations; fallback priority is live, case study, download, code. Records with no action display readable content without a dead button.

Project records with `sourcePath` generate detail pages from the corresponding manifest. A new standalone app only needs its public URL. No iframe coupling or third-party dashboard dependency is necessary.

## Source structure
```text
content/projects.json
schemas/project.schema.json
templates/{home,gallery,project}.html
scripts/{build_site,check_site}.py
site/
  index.html
  assets/{site.css,site.js,favicon.svg}
  work/<slug>/index.html
  privacy/index.html
  404.html
.github/workflows/site.yml
```
The project repository also retains the engine, controls, collectors, policies, examples and tests.

## Publishing and rollback
Publish only `site`. Keep credentials, raw evidence and client documents outside it. Git pushes trigger builds when Pages Git integration is configured. Roll back using the previous successful Pages deployment or revert the corresponding Git commit. Themes and browser navigation require JavaScript; content and case studies are readable without it. Reduced-motion and print styles are included.

## Boundaries
The public system is a portfolio and local decision-support interface, not a hosted multi-tenant evidence service. No fabricated client outcomes, certification, experience or legal-compliance conclusions are presented. Sample assessments are clearly identified. Private client processing requires separate authentication, authorization, data-retention and confidentiality controls.
