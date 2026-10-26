# NGTS skills

Skills for the NGTS API (Palo Alto Networks Strata Cloud Manager certificate management).
The skills themselves live in [`skills/`](../skills/) so that `install.py` finds them:

```bash
python install.py --install "ngts-*"     # also copies skills/_shared next to them
```

| Skill | Covers |
|---|---|
| [`_shared`](../skills/_shared/) | API conventions, GraphQL/gateway behavior, glossary, OpenAPI source map (read by every NGTS skill) |
| [`ngts-auth-access`](../skills/ngts-auth-access/) | OAuth tokens, TSG discovery, NGTS Built-in Accounts |
| [`ngts-certificate-governance`](../skills/ngts-certificate-governance/) | Issuing templates (request policies), Built-in PKI issuance policies, approval rules, workload policies |
| [`ngts-certificate-inventory`](../skills/ngts-certificate-inventory/) | Existing certificates, TLS endpoints, discovery, tags, renewal monitoring |
| [`ngts-certificate-provisioning`](../skills/ngts-certificate-provisioning/) | Certificate import and requests, SCEP servers and SCEP enrollment diagnosis |
| [`ngts-issuers`](../skills/ngts-issuers/) | Distributed issuers, sub-CA providers, Built-in PKI root/sub-CA creation and decommission |
| [`ngts-machines-connectors`](../skills/ngts-machines-connectors/) | Machines, connectors, credentials, VSatellites |
| [`ngts-platform-ops`](../skills/ngts-platform-ops/) | Activity and audit logs |

Live-verified (2026-10-25): `ngts-issuers/references/builtin-pki.md`,
`ngts-certificate-governance/references/issuance-and-request-policies.md`,
`ngts-certificate-provisioning/references/scep-servers.md`, and the GraphQL section of `_shared/conventions.md`.
