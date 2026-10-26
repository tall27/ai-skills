---
name: ngts-auth-access
description: Obtain or troubleshoot NGTS API OAuth access; explain TSG and SCM service-account setup; manage NGTS Built-in Accounts, scopes, credentials, or OCI tokens. Do not use for certificate issuance, inventory, or machine management.
---

# NGTS authentication and access

Read `../_shared/conventions.md` before any API call. Read `../_shared/glossary.md` when account types are unclear.

## Scope

- SCM OAuth client-credentials tokens for NGTS API.
- NGTS Built-in Account lifecycle, scopes, credential rotation, OCI token regeneration.

**Boundary:** SCM service account obtains bearer token. `/v1/serviceaccounts` manages different NGTS Built-in Accounts. Do not conflate them.

## Workflows

### Obtain API access

1. Confirm TSG exists and record `tsg_id`.
2. Confirm SCM service account belongs to TSG and has least-privilege role.
3. Exchange `client_id`/`client_secret` for token using conventions reference.
4. Run read-only NGTS call before mutations.
5. Cache token only in process memory; renew before 15-minute expiry.

### Rotate Built-in Account credentials

1. Get account and scopes first.
2. Confirm account ID, intended consumer, and rotation impact.
3. Rotate credentials with documented endpoint.
4. Store returned secret in approved secret manager; do not print it.
5. Validate dependent integration using new credential.

Full operations: `references/endpoints.md`.
