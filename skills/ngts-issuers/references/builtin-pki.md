# Built-in PKI: create and remove CA hierarchies (GraphQL)

Verified live 2026-10-25 on a TEST-tier PKI configuration, with a service-account token on
`https://api.strata.paloaltonetworks.com/ngts/graphql`. Payloads were taken from UI HARs.
Read `../../_shared/conventions.md` (gateway behavior).

## Model

- A tenant has PKI configurations: `pkiConfigurations(first:) { nodes { id name tier } }`, usually `Test` (`tier: TEST`) and `Production`.
- Every change is a **proposed change**: `createPKIProposedChange(input:{configurationID, name, proposedChange:{...}})` returns `proposedChange { id errors { message } }`. It is then applied with `applyPKIProposedChange(input:{id})`. `applyImmediately: true` and `dryRun` also exist (not used here).
- `proposedChange` content lists: `keypairs`, `certificates`, `issuers`, `ocspResponders`, `crlDistribution`, `issuancePolicies`, `approvalRules`, `decommissionedArtifacts`, `externalCertificates`.
- Within one change, a definition can reference another by its `name`. Across changes, use the definition ID `<configID>/history/<changeName>/<Type>/<defName>` (e.g. `.../Certificate/test01-x`) or the artifact ID `<configID>/<Type>/<n>`.
- Change names must be unique per configuration. The UI appends a random 5-character suffix (`add-ca-test01-qf9qh`).
- **The configuration runs one provisioning workflow at a time.** A second create/apply right after an apply fails with `A provisioning workflow is already running for this configuration; retry later`. Retry every ~2s; the wait is typically under 10s.

## Create a root + issuing sub-CA

1. Key storage: `keyStorageLocations(first:50, capabilities:{keyCreation:true, sign:true}) { nodes { id name driver { id } } }`. The location named `Default` is what the UI uses.
2. Root change. A CA certificate plus an OCSP keypair/cert, the OCSP responder and the CRL distribution point:
   - keypair `{name, parameterSet:"KeyParameterSetRsa4096", driverID, locationID, keyUsages:["KEY_CERT_SIGN","CRL_SIGN"]}`
   - OCSP keypair: `keyUsages:["DIGITAL_SIGNATURE"]`, `extendedKeyUsages:["1.3.6.1.5.5.7.3.9"]`
   - certificate `{name, isCA:true, keypairID, signatureAlgorithm:"1.2.840.113549.1.1.12", subjectDN, validityDuration:"P6Y", crlDistributionPointIDs:[<crl>], ocspResponderIDs:[<ocsp>], constraints:{pathLength:3}}`
   - OCSP cert `{isCA:false, parentID:<ca name>, validityDuration:"P1Y", subjectDN:"CN=OCSP Responder,<ca dn>", extensions:[{oid:"1.3.6.1.5.5.7.48.1.5", critical:false, value:"BQA="}]}` (that extension is OCSP no-check)
   - `ocspResponders:[{name, certificateID:<ocsp cert>}]`, `crlDistribution:[{name, certificateID:<ca>}]`
3. Sub-CA change: the same shape, RSA-2048, `P3Y`, without `constraints`, with `parentID` set to the **root definition ID**, plus `issuers:[{name, displayName, certificateID:<sub ca name>}]`. Without the issuer, the CA cannot issue end-entity certificates.
4. On the TEST tier, CA names in the UI start with `test` (`test01`, `test-sub-ca-01`). Keep that prefix.

## Link the issuer to templates

- Poll `pkiConfiguration(input:{id}) { roots(includeAll:true) { ... on PKICertificateArtifact { children { ... on PKICertificateArtifact { definition { name } issuingCAs { status caOpsID } } } } } }` until the sub-CA's `issuingCAs[].caOpsID` is set (about 3–5s after apply).
- `caOpsID` **is** the CA account ID of type `BUILTIN_GEN2`: `GET /v1/certificateauthorities/BUILTIN_GEN2/accounts/{caOpsID}` returns `productOptions[0].id`, which is the `certificateAuthorityProductOptionId` that issuing templates need. The same response has `account.accountDetails.builtinGen2CaId` (`caId` for `issuancePoliciesForCA`).

## Remove (decommission)

- Send one proposed change: `decommissionedArtifacts:[{name, ids:[...], note}]`. `ids` accepts definition IDs, so store them at creation time and no lookup is needed.
- **Dependents cascade**: decommissioning the root takes the sub-CA, issuer, OCSP and CRL objects with it. Issuance policies can go in the same `ids` list.
- Decommissioned CAs stay visible in `roots(includeAll:true)` with `status: DECOMMISSIONED`.
- Order for a full SCEP stack: deactivate the SCEP server, delete the issuing templates (REST `DELETE`), then decommission the policies and the root.
