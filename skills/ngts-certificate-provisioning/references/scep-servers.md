# NGTS SCEP servers (GraphQL)

Verified live 2026-10-25 against a TEST-tier tenant.
Client side (verified): AES-128 envelope + SHA-256 signatures (DES/SHA-1 get 403), encrypt to the RA *encryption* cert only,
keep the temporary signer cert serial positive, send no SAN `extensionRequest` (HTTP 500).

## Feature check

`{ searchSCEPServers(first:1) { nodes { id } } }` returns `"Feature not available yet"` (code 65012) when SCEP is not enabled on the TSG. Run this check before creating anything.

## Create

```graphql
mutation($input: CreateSCEPServerInput!) { createSCEPServer(input: $input) {
  scepServer { id name directoryURL raStatus }
  credential { __typename ... on SCEPChallengeCredential { challenge } } } }
```

Input: `{ name, endEntityIssuingTemplateID, raSigningIssuingTemplateID, raEncryptionIssuingTemplateID, authentication: { methodType: "STATIC" } }`.

- **Three issuing templates** are required (see `../../ngts-certificate-governance/references/issuance-and-request-policies.md`). They should share one CA so the RA certificates chain.
- Static auth: the challenge is returned **once**, in this response. Store it right away (DPAPI or a secret store).
- Dynamic auth: `methodType: DYNAMIC` with `method: SERVICE_ACCOUNT` (`credentialGeneration: CUSTOM|SYSTEM`) or `HEADER_TOKEN`. Not tested live.
- `directoryURL` is the SCEP URL for clients: `https://<tsg>.ngts.paloaltonetworks.com/v1/scep/<companyId>/<serverId>`.
- `raStatus` was already `ready` when checked a minute later. GetCACert returns 4 certs: RA signing, RA encryption, the issuing CA and the root.

## Read

`SCEPServer(id:) { id name raStatus deactivated endEntityIssuingTemplate { id name } raSigningIssuingTemplate { id name } raEncryptionIssuingTemplate { id name } }`. The template sub-fields work even though the SDK query does not select them. Use them to find which templates a working server uses.

## Remove

`mutation($id: ID!) { deactivateSCEPServer(id: $id) }`. There is no delete mutation (`deleteSCEPServer` returns gateway 403). Deactivation removes the server from the UI, so treat it as delete. `searchSCEPServers` still lists it with `deactivated: true`. Deactivate it before deleting its templates.

## Diagnosing enrollment failures

- First, run the same client against a known-good server. If that works, the problem is the new server's configuration, not the client.
- HTTP 500 "Internal error" at PKIOperation can mean the CSR violates the end-entity template's subject regexes (e.g. L regex `Chicago`, CSR without L). These requests never appear in `POST /outagedetection/v1/certificaterequestssearch`, because the failure happens before a request is created.
- Isolate the cause with a hand-built CSR, changing one subject attribute per run.
