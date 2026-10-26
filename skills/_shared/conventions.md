# NGTS API conventions

Last verified: 2026-07-31.

## Endpoints and authentication

- NGTS API base URL: `https://api.strata.paloaltonetworks.com/ngts`.
- OAuth token endpoint: `POST https://auth.apps.paloaltonetworks.com/oauth2/access_token`.
- Token request uses HTTP Basic authentication: `client_id:client_secret`.
- Send form body: `grant_type=client_credentials&scope=tsg_id:<tsg_id>` with `Content-Type: application/x-www-form-urlencoded`.
- Send every NGTS request with `Authorization: Bearer <access_token>`.
- Send `Accept: application/json`; send `Content-Type: application/json` for JSON bodies.
- Access tokens expire after 15 minutes. Reuse token, renew before expiry, and renew after `401 Unauthorized`.

Never put client secrets, access tokens, private keys, pairing codes, recovery codes, or credential values in source control, logs, or chat output.

## Request behavior

- API payloads use JSON and camel-case property names.
- `application`, `applications`, `team`, and `teams` compatibility fields can appear in schemas but NGTS ignores or omits them.
- Paths under `/v1/serviceaccounts` manage NGTS **Built-in Accounts**, not SCM IAM service accounts.
- Use documented `limit` and `offset` pagination where endpoints expose them. Default page size in SCM guidance is 200; stop after empty or short page.
- Prefer documented server-side filters/search endpoints over client-side filtering.
- Validate returned IDs/statuses before issuing a dependent mutation.
- Documentation gives diagnostic errors but no universal NGTS error catalog, retry policy, rate-limit policy, or idempotency key. Set client timeouts and do not assume retries are safe for mutations.

## GraphQL and gateway behavior (verified live 2026-10-25, service-account token)

- GraphQL: `POST https://api.strata.paloaltonetworks.com/ngts/graphql`, body `{query, variables}`, same Bearer token. The UI uses `api.apps.paloaltonetworks.com/ngts/graphql`, and UI HAR payloads replay unchanged on `api.strata`.
- Built-in PKI, issuance policies and SCEP servers exist **only in GraphQL**. Issuing templates are created through REST.
- The gateway allowlists operations. Introspection (`__type`) and unknown root fields return **HTTP 403 `AUTHZ_DENIED`**, not a GraphQL error. Do not read 403 as a missing role: copy the operation from a UI HAR or from the ngts SDK (`ngts/_graphql/client.py` in the ngts-claude-plugin venv).
- `"Feature is not available"` (code 20055) or `"Feature not available yet"` (code 65012) on `pkiConfiguration(s)` / `searchSCEPServers` means the feature is off for **that TSG**. Check the TSG before blaming credentials.
- `GET /v1/certificateissuingtemplates` and `GET /v1/certificateissuingtemplates/{id}` return **404 with an empty body** to a service account, while `POST` and `DELETE` on the same paths work. To read templates, use GraphQL `issuingTemplates(first:) { nodes { id name validityPeriodInSeconds certificateAuthorityAccount { id name } } }`.
- Async apply: anything created through a PKI proposed change becomes visible a few seconds later. Poll for it; do not read it once and fail.
- PowerShell clients: `$(if (...) { @('x') })` unrolls a one-element array into a scalar, and an empty one into `$null`. NGTS REST then answers `1006 "request object parsing failed"`. Wrap the result: `@($(if (...) { 'x' }))`.

## Safe mutation order

1. List/get target and confirm scope.
2. Validate payload if a validation endpoint exists.
3. Use create/update action.
4. Re-read target or workflow/status result.
5. For deletion, retirement, revocation, credential rotation, or code generation: show exact target and effect before action.

## Sources

- https://pan.dev/scm/api/config/ngts/ngts-api/
- https://pan.dev/scm/docs/access-tokens/
- https://pan.dev/scm/docs/api-call/
- https://pan.dev/scm/docs/api-best-practices/
