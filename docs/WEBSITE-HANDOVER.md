# Website handover

Edit public copy in `templates/`, project records in `content/projects.json`, and shared design tokens in `site/assets/site.css`. Generated HTML should be rebuilt after template or catalogue changes.

Run `npm run build` followed by `npm test`. Preview `site/` using a local HTTP server. Check desktop and mobile, both themes, keyboard focus, filters and the email brief before publishing.

Deploy the `site` directory. Existing paths, form field names, legal/privacy copy and project records are preserved. The contact form opens the visitor's email application; it is not a server submission.

Public scenarios are synthetic. Counts describe portfolio scope, not client outcomes. Add testimonials, client logos or delivery savings only when verified and authorized.

For new projects, follow the existing catalogue fields and manifest structure. Keep a Git commit before each update to allow rollback. Support duration and maintenance terms are agreed per engagement; this site does not promise an unstaffed support window.

## Connected portfolio and display settings

Project sections are consolidated into in-page disclosures by `scripts/page_sections.py` in the project repository. Former section URLs redirect to the corresponding anchors on Cloudflare Pages and Vercel. Add related project slugs in the catalogue to maintain onward paths. Appearance controls preserve theme, text size and spacing in the visitor browser. The connected scenario can be loaded explicitly from the suite and provides 16 linked, illustrative record types.
