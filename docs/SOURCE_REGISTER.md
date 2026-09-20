# Research and source register

Research date: 17 September 2026.

Use primary sources for technical and regulatory claims. Recheck versions before a production release.

| Topic | Primary source | Implementation consequence |
|---|---|---|
| OSCAL | https://pages.nist.gov/OSCAL-Reference/models/v1.2.3/ | Component definitions declare OSCAL 1.2.3 |
| NIST AI RMF | https://www.nist.gov/itl/ai-risk-management-framework | Registry treats AI RMF 1.0 as a current voluntary framework while tracking NIST revision work |
| ISO/IEC 42001 | https://www.iso.org/standard/81230.html | Project 2 maps AI management-system capabilities without claiming certification |
| EU AI Act consolidated text | https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng | Project 6 treats Article 50 disclosure and marking as product release evidence, with legal review |
| MCP specification | https://modelcontextprotocol.io/specification/2026-07-28 | MCP uses the current stateless-core specification and narrow tool contracts |
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk | Service pins the stable v2 major range |
| Open Policy Agent | https://github.com/open-policy-agent/opa/releases | Compose pins OPA 1.20.2 and uses Rego v1 syntax |
| GitHub Actions checkout | https://github.com/actions/checkout/releases | Workflows use checkout v7 |
| GitHub Actions setup-python | https://github.com/actions/setup-python/releases | Workflows use setup-python v7 |
| GitHub immutable releases | https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases | Evidence workflow uses draft, upload, publish and never edits history |
| Cloudflare Pages limits | https://developers.cloudflare.com/pages/platform/limits/ | Static portal fits the free Pages deployment model |
| Cloudflare Workers limits | https://developers.cloudflare.com/workers/platform/limits/ | Optional facade must fit free request and CPU limits; static hosting remains the default |
| NIST CSF 2.0 | https://www.nist.gov/cyberframework | Registry includes CSF 2.0 as a broad security governance candidate |
| GDPR Article 28 | https://eur-lex.europa.eu/eli/reg/2016/679/oj | Project 9 routes contract sufficiency and role questions to qualified review |

The repository deliberately avoids copying copyrighted standards text. It stores short control titles, internal test logic, identifiers, and links to authoritative sources. Licensed ISO requirements must be obtained and used under the organisation's license.
