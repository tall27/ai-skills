# Auth and Built-in Account endpoints

Base URL: `https://api.strata.paloaltonetworks.com/ngts`. OAuth token source: `https://auth.apps.paloaltonetworks.com/oauth2/access_token`. Read `../../_shared/conventions.md`.

## OAuth token

| Method | URL | Request | Response |
|---|---|---|---|
| POST | `https://auth.apps.paloaltonetworks.com/oauth2/access_token` | HTTP Basic `client_id:client_secret`; form `grant_type=client_credentials`, `scope=tsg_id:<tsg_id>` | OAuth access token; 15-minute lifetime |

## TSG discovery (verified live 2026-10-25)

- An SCM service-account Client ID contains its home TSG: `<name>@<tsg_id>.iam.panserviceaccount.com`. Get the first token with that TSG; there is no need to ask for a TSG ID.
- List the TSGs the account can reach with `GET https://api.strata.paloaltonetworks.com/tenancy/v1/tenant_service_groups?hierarchy=true`. The response is `{items:[{id, display_name, parent_id, children:[...]}]}`, a nested tree, so walk `children` recursively.
- An account that lives in a parent TSG can get a token for a child TSG: `scope=tsg_id:<child>`. Both the home-TSG token and the child-TSG token return the full tree from `tenant_service_groups`. For NGTS calls, use a token scoped to the target tenant.
- Before blaming credentials, check that the TSG is the right one. Creds for tenant A answer `Feature is not available` for PKI/SCEP on tenant B (see `../../_shared/conventions.md`).

## NGTS Built-in Accounts

These endpoints do **not** manage SCM IAM service accounts.

| Method | Path | Operation | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/serviceaccounts` | List accessible accounts | None | `GetServiceAccountsResponseBody` |
| POST | `/v1/serviceaccounts` | Create account | `CreateServiceAccountRequestBody` | `CreateServiceAccountResponseBody` (`201`) |
| GET | `/v1/serviceaccounts/{id}` | Get account | Path `id` | `GetServiceAccountsByClientIDResponseBody` |
| PATCH | `/v1/serviceaccounts/{id}` | Update account | Path `id`; `PatchServiceAccountByClientIDRequestBody` | `204` |
| DELETE | `/v1/serviceaccounts/{id}` | Delete account | Path `id` | `204` |
| GET | `/v1/serviceaccounts/scopes` | List supported scopes | None | `GetServiceAccountScopesResponseBody` |
| PUT | `/v1/serviceaccounts/{id}/ocitoken` | Regenerate OCI registry token | Path `id` | `PutServiceAccountByClientIDOCITokenResponseBody` |
| PUT | `/v1/serviceaccounts/{id}/credentials` | Rotate/update account credentials | Path `id`; `PutServiceAccountByClientIDCredentialsRequestBody` | `PutServiceAccountByClientIDCredentialsResponseBody` |

Source: [NGTS OpenAPI](https://raw.githubusercontent.com/PaloAltoNetworks/pan.dev/master/openapi-specs/scm/config/ngts/tlsprotect-cloud.json).
