# Organization evaluation deployment

The public portfolio, suite and workspace remain independently accessible. `/evaluate/` uses Cloudflare Pages Functions only when organization access, a D1 database and a processing provider are configured. A static-only host displays the access-request route. No active subscription, production identity connection or partner processing is claimed by committing this source.

## Access and provisioning

Create a Cloudflare Access application covering `/api/account`, `/api/login` and `/api/evaluate`. Keep `/api/status` publicly reachable. Set `ACCESS_ISSUER` to the Access team HTTPS origin and `ACCESS_AUDIENCE` to the application's audience tag. The handler validates RS256 signature, issuer, audience, expiry and subject; unsigned headers, self-declared domains, IP addresses and browser counters do not authorize access.

Bind a D1 database as `GRC_DB` and apply `migrations/0001_evaluations.sql`. Enroll verified identity subjects in `members` after confirming organization membership. Different users in an organization map to the same internal tenant. Tenant membership is provisioned by the owner, never inferred from an email domain or accepted from client JSON. Test the Access login path and exact issuer format before enabling access.

The default allowance is **two successful or pending evaluations per tenant**, shared across browsers and members. A single conditional SQLite insert reserves a credit atomically. Completed retries with the same request ID return the stored report; a mismatched payload returns a conflict. Failed provider requests release the allowance. Pending records after interrupted execution require operator reconciliation; do not release them until checking upstream execution and report delivery.

## Provider contract and data handling

Set secret `PROVIDER_KEY`, HTTPS `PROVIDER_URL` and public `PROVIDER_LABEL`. Use a vetted server-side adapter with the following JSON contract:

- Request: `{system: string, input: {scope, context, domains}}`
- Response: `{findings: [{domain, finding, evidenceNeeded, nextAction, owner}]}`

The endpoint is configured by the operator, not supplied by visitors. Keys never appear in browser code. The interface identifies the processor and requires authorization for sanitized inputs. Agree subprocessors, storage location, retention and deletion before provisioning clients. Do not hide material third-party processing or invent compliance/certification outcomes. The service stores membership, usage, input hashes and completed reports; avoid sensitive context and operational secrets.

## Paid access

No payment provider or subscription webhook is connected. Quota exhaustion returns HTTP 402 and directs the organization to a real contact page. After verifying a purchased engagement, the owner can provision an agreed additional allowance. Never use an unverified checkout redirect or client-side plan flag to grant entitlement. Automated subscriptions require a separate billing integration with signed webhooks, idempotent events, cancellation/revocation and entitlement reconciliation before advertising them.

## Hosting and verification

Pages Functions live in `functions/` and deploy with Cloudflare Pages. Configure D1 bindings through the Cloudflare dashboard or a valid Wrangler binding with the real database ID; no invented IDs are included here. Vercel and GitHub Pages host the public static content only in this implementation. Do not describe the protected service as live there without deploying an equivalent backend.

Run `npm test`, `python -m unittest discover -s tests -v`, and `python scripts/validate_repository.py`. Then verify deployed sign-in, member isolation, simultaneous quota reservations, report retries, provider timeout, and data deletion against the configured environment. Access policy, database provisioning, real provider behavior, live rendering and payment integration cannot be verified solely by local unit tests.

Primary documentation: https://developers.cloudflare.com/pages/functions/bindings/ and https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/ .
