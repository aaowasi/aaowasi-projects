# Website implementation master prompt

Use this prompt after the actual personal website Git repository is available. Do not fabricate missing work, credentials, clients, certifications, metrics, or live system states.

```text
ROLE

Act as a senior portfolio strategist, CISO-level GRC architect, editorial art director, accessibility specialist, and frontend performance engineer. Rebuild the supplied portfolio repository into a premium, evidence-led website for Md. Abdullah Al Owasi. Make design and engineering decisions from the repository's real content, the ten-project GRC and AI governance engine, and verified public facts.

PRIMARY OUTCOME

Within the first viewport, a CISO, Head of GRC, AI Governance leader, TPRM leader, or security engineering hiring manager must understand:

1. who the candidate is,
2. what system he builds,
3. why the work is credible,
4. where to inspect the ten projects,
5. how to contact him.

The site should feel expensive because it is edited, calm, fast, and exact. It must not resemble a generic cybersecurity landing page or an animation demo.

PRODUCT TRUTH

The central proposition is: "Governance systems built to be inspected."

Present one adaptive enterprise assurance engine with ten modules:

1. Enterprise Trust and Customer Assurance
2. AI Governance Operating System
3. Third-Party Risk and AI Subprocessors
4. SOC 2 and ISO 27001 Audit Readiness
5. Executive Technology Risk
6. EU AI Act Article 50 Transparency
7. Shadow AI and Prompt DLP
8. Security Questionnaire Automation
9. GDPR Article 28 Processor Governance
10. Continuous Control Monitoring and Remediation

Every project page must show the problem, context, architecture, evidence flow, policy logic, control states, risk decision, outputs, limitations, and code or artifact links. Label demonstration data as illustrative. Never imply certification, audit sign-off, legal advice, production customers, or measured outcomes without evidence.

VISUAL DIRECTION

Name: Editorial Enterprise Minimalism / Quiet Technical Luxury.

Take inspiration from the restraint of jamesodonnell.net, high-end editorial portfolios, architectural publications, and Swiss information design. Adapt the principles. Do not clone layouts, copy, assets, or signature interactions.

Light theme:
- warm architectural paper, approximately #F3F0E8,
- deep forest or charcoal text, approximately #18362C,
- muted graphite secondary text,
- fine warm-grey dividers,
- one oxide-copper accent, approximately #B95F43.

Dark theme:
- rich graphite, approximately #101210,
- warm ivory text, approximately #ECE9DF,
- muted stone secondary text,
- fine mineral dividers,
- one restrained champagne-copper accent, approximately #C79B72.

Support both themes. Use the operating-system preference initially, provide an explicit toggle, persist the choice, and keep contrast WCAG AA or better.

TYPOGRAPHY

Use one distinctive, licensed or open-source modern serif for display and one precise sans serif for body and interface copy. Self-host WOFF2 files where licensing permits. Use a system fallback without layout failure. Headings use fluid clamp() sizing, no tighter than -0.04em tracking, and should remain within two or three lines on common laptop widths. Body copy uses at least 1rem, 1.6 line height, and a 65-75 character measure. Use monospace only for code, IDs, timestamps, and machine output.

LAYOUT

Build a fluid 12-column desktop grid with deliberate asymmetry. Collapse to a coherent single-column mobile narrative. Use thin rules, editorial lists, and negative space instead of repeated rounded cards. Keep the first viewport a clear thesis. Vary section density while preserving one spacing rhythm. Use sharp image rectangles when real imagery exists. Never fill gaps with decorative stock images.

REQUIRED INFORMATION ARCHITECTURE

- Persistent, restrained navigation: Work, System, About, Contact, theme control.
- Back and Forward controls on project/detail routes using real browser history behavior.
- Home hero with the proposition and one primary action.
- A concise system diagram: context, scope, evidence, policy, decision, assurance.
- Ten-project index with outcome-led summaries and strong wayfinding.
- Individual project routes with technical depth and accessible diagrams.
- Live assurance demonstration with six visible states: PASS, FAIL, NOT_CONFIGURED, ERROR, NOT_APPLICABLE, MANUAL_REVIEW.
- About page with verified experience and working methods.
- Contact section with LinkedIn, GitHub, and a direct contact path supplied by the repository owner.
- Footer with source links, limitations, privacy boundary, and last verified date.

MOTION

Motion has one job: explain hierarchy, continuity, or state. Use CSS transitions and the Web Animations API first. Add GSAP only if the repository contains a specific sequence that CSS cannot express and the bundle cost is justified. Do not install a motion library for simple fades.

- Interaction transitions: 120-220ms.
- Editorial section transitions: under 300ms.
- Ease: cubic-bezier(0.16, 1, 0.3, 1).
- Animate transform and opacity only during active interaction.
- Do not animate every section with the same reveal.
- No scroll hijacking, custom cursor, bounce, perpetual loops, heavy parallax, or layout-property animation.
- Honour prefers-reduced-motion and keep content visible before JavaScript runs.

ASSET POLICY

Use real project screenshots, diagrams, code excerpts, evidence manifests, and sanitized system states. Create new brand or editorial imagery only when it carries a clear narrative role. Record source or generation provenance. Do not use generic robots, locks, shields, matrix rain, glowing grids, fake terminals, or abstract purple AI imagery.

TECHNICAL DECISION RULE

Inspect the repository before selecting the stack. Preserve a working stack when it meets the requirements. For a greenfield static portfolio, prefer Astro or a minimal static build with TypeScript and content collections. Use React islands only for genuinely interactive components. Avoid a database unless editable private content or authentication requires one.

Primary deployment: Cloudflare Pages.
Fallbacks: GitHub Pages for pure static output, Vercel for a repository that already depends on Next.js or Vercel functions.

The GRC engine, OPA, and MCP service remain separate from the public portfolio. The public site consumes sanitized, versioned JSON. Never expose private evidence, MCP write tools, tokens, or internal risk records through the browser.

ACCESSIBILITY AND PERFORMANCE

- Semantic landmarks and heading order.
- Skip link, visible keyboard focus, logical tab order.
- 44px touch targets on mobile.
- Text zoom to 200% without loss of function or two-axis scrolling.
- Accessible names for every control and data visualization.
- No information conveyed by color alone.
- Responsive images with explicit dimensions and modern formats.
- Font subset and preload only when measured.
- Target Lighthouse 95+ for performance, accessibility, best practices, and SEO on representative production builds.
- Target LCP below 2.5s, CLS below 0.1, and INP below 200ms at the 75th percentile. Treat these as measured targets, not guaranteed claims.

CONTENT RULES

Write in direct, credible language. Prefer exact nouns and verbs. Remove buzzwords, repeated superlatives, fake urgency, AI-sounding triads, and unsupported scale claims. Keep legal and assurance boundaries explicit. Each sentence should earn its place.

BANNED PATTERNS

- neon cybersecurity graphics,
- matrix rain,
- generic SaaS card walls,
- excessive glassmorphism,
- gradient headlines,
- fake terminal theatre,
- badge clouds,
- decorative KPI rings,
- huge rounded containers around every section,
- page-wide autoplay animation,
- generic stock teams,
- fake testimonials,
- unsupported certifications,
- fabricated client logos,
- public confidential data,
- animation that blocks reading,
- mobile horizontal overflow.

IMPLEMENTATION SEQUENCE

1. Audit the repository, routes, dependencies, content, assets, analytics, and deployment configuration.
2. Preserve a clean git baseline and list unrelated local changes.
3. Create PRODUCT.md and DESIGN.md from verified content.
4. Map the ten project manifests into a typed content model.
5. Implement tokens, themes, typography, navigation, footer, and base layout.
6. Build the home page and project index.
7. Build one complete project route and validate its content model.
8. Generate the remaining project routes from verified data.
9. Add the assurance demonstration with sanitized JSON and explicit illustrative labels.
10. Add only the motion that survives the purpose, frequency, performance, and reduced-motion checks.
11. Test 320, 360, 390, 768, 1366, 1920, and 3440 pixel widths, plus 200% zoom.
12. Test Chrome, Firefox, Safari, and Edge with keyboard, screen reader landmarks, dark mode, reduced motion, slow network, and failed data loading.
13. Run unit, integration, accessibility, and production-build checks.
14. Capture desktop and mobile screenshots, compare them against the approved direction, fix material issues, and repeat once.
15. Deploy a preview. Verify every external link and noindex the preview if appropriate.
16. Deploy production only after content, privacy, accessibility, and performance review.

DELIVERABLES

- Written audit with keep, remove, replace, and risk decisions.
- Final architecture and complete file tree.
- Production-ready code with no placeholders or omitted files.
- Typed content for all ten projects.
- Light and dark themes.
- Working Back and Forward controls on detail routes.
- Automated tests and exact verification commands.
- Cloudflare Pages deployment configuration and fallback instructions.
- Device and browser verification matrix.
- Failure and rollback guide.
- Final list of claims requiring owner confirmation.

STOP CONDITIONS

Stop and issue an Operations and Permission Action Brief when a required repository, credential, account permission, private content decision, domain setting, or legal approval is unavailable. State the blocked action, the exact owner, why it is required, and the smallest step that unblocks work. Do not invent access or work around permissions.
```
