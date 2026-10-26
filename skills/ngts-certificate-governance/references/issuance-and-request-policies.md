# Issuance policies + request policies (issuing templates) for Built-in PKI CAs

Verified live 2026-10-25. Payloads were taken from UI HARs.
CA creation and the `caOpsID` → product option lookup are in `../../ngts-issuers/references/builtin-pki.md`.

## Terms

- **Issuance policy**: a PKI-side constraint document (key algorithms, validity bounds, KU/EKU, subject DN and SAN rules). GraphQL only; it is created inside a PKI proposed change.
- **Request policy**: the UI name for an **issuing template** (REST `/v1/certificateissuingtemplates`). A template points at one issuance policy (`product.issuancePolicyId`) and one CA product option.

## Create issuance policies

`createPKIProposedChange` with `proposedChange.issuancePolicies:[...]`, then `applyPKIProposedChange`. One change can carry several policies (three verified).

```json
{ "name": "demo SCEP RA Signing", "description": "...", "category": "SERVER_AND_INFRASTRUCTURE", "platformTier": "TEST",
  "constraints": { "schemaVersion": 1,
    "validity": { "minimum": "P1D", "maximum": "P730D", "default": "P365D" },
    "keyAlgorithms": [{ "permittedParameterSets": ["KeyParameterSetRsa2048","KeyParameterSetRsa3072","KeyParameterSetRsa4096"],
                        "selectedSecurityTiers": ["TIER_1","TIER_2"] }],
    "keyUsage": [{ "behavior": "REQUIRED", "values": ["DIGITAL_SIGNATURE"] }],
    "extendedKeyUsage": [{ "behavior": "REQUIRED", "values": ["SERVER_AUTH"] }],
    "basicConstraints": { "isCA": false },
    "subjectDn": [{ "attribute": "CN", "behavior": "REQUIRED", "allowedValues": [], "defaultValues": [], "minOccurrences": 0, "maxOccurrences": 1 }, "... O/OU/L/ST/C OPTIONAL"],
    "subjectAltNames": [{ "sanType": "DNS_NAME", "behavior": "FORBIDDEN", "allowedValues": [], "minOccurrences": 0, "maxOccurrences": 10 }, "... IP_ADDRESS/EMAIL/URI"] } }
```

- `category`: `SERVER_AND_INFRASTRUCTURE` | `IDENTITY_AND_USER_AUTHENTICATION` | `NETWORK_AND_DEVICE_ACCESS`. `behavior`: `REQUIRED` | `OPTIONAL` | `FORBIDDEN`.
- Getting `policyId` after apply: the policy appears **asynchronously**. Poll `issuancePolicies(first:500, input:{}) { nodes { policyId artifactId name kind } }` and match by name. Reading `issuancePoliciesForCA(input:{caId})` once, right after apply, did not return the new policies.
- `kind: TEMPLATE` entries (ready-made, `artifactId: null`) and `kind: CUSTOM` (yours) are listed together.
- Remove: `decommissionedArtifacts` with the definition IDs `<configID>/history/<changeName>/IssuancePolicy/<policy name>`.

## Create request policies (issuing templates)

`POST /v1/certificateissuingtemplates` returns `201 {certificateIssuingTemplates:[{id,...}]}`; delete with `DELETE /v1/certificateissuingtemplates/{id}`. Service-account `GET` returns 404; see conventions.

```json
{ "name": "demo SCEP RA Signing", "description": "", "certificateAuthority": "BUILTIN_GEN2",
  "product": { "certificateAuthority": "BUILTIN_GEN2", "productName": "Default Product", "productTypes": ["SSL","CODESIGN"],
               "validityPeriod": "P365D", "issuancePolicyId": "<policyId>" },
  "certificateAuthorityProductOptionId": "<productOptions[0].id of the BUILTIN_GEN2 account = issuer caOpsID>",
  "subjectCNRegexes": [".*"], "subjectORegexes": [".*"], "subjectOURegexes": [".*"], "subjectLRegexes": [".*"],
  "subjectSTRegexes": [".*"], "subjectCValues": [".*"],
  "keyAlgorithmTypes": [{ "keyType": "RSA", "keyLengths": [2048,3072,4096] }, { "keyType": "EC", "keyCurves": ["P256","P384"] }],
  "keyUsageValues": ["DIGITAL_SIGNATURE"], "extendedKeyUsageValues": ["SERVER"], "customExtendedKeyUsageOidValues": [],
  "keyReuse": false, "csrUploadAllowed": true, "keyGeneratedByVenafiAllowed": false, "driverGeneratedCsr": false,
  "shareWithAll": false, "consumerTsgIds": [], "everyoneIsConsumer": false, "resourceConsumerUserIds": [], "resourceConsumerTeamIds": [] }
```

- `certificateAuthorityAccountId` is not sent; the product option implies it.
- Template EKU names differ from policy EKU names: `SERVER`/`CLIENT` in the template vs `SERVER_AUTH`/`CLIENT_AUTH` in the policy.
- Device templates add `sanRegexes` / `sanUniformResourceIdentifierRegexes: [".*"]` when the policy allows those SANs.
- Every regex/list field must be a JSON **array**. A bare string gives `1006 "request object parsing failed"`.

## SCEP set (3 policies + 3 templates per server)

| Role | Policy KU / EKU | Template KU / EKU | Validity |
|---|---|---|---|
| RA signing | DIGITAL_SIGNATURE / SERVER_AUTH | DIGITAL_SIGNATURE / SERVER | P365D (max P730D) |
| RA encryption | KEY_ENCIPHERMENT / SERVER_AUTH | KEY_ENCIPHERMENT / SERVER | P365D (max P730D) |
| Devices (end entity) | DIGITAL_SIGNATURE+KEY_ENCIPHERMENT / CLIENT_AUTH, RSA+EC P-256/P-384, SAN DNS+URI optional | same / CLIENT | P90D (max P200D) |

RA SANs are FORBIDDEN, and RA keys are RSA only.

## Gotcha: subject regexes vs SCEP CSRs

A template with `subjectLRegexes: ["Chicago"]` (the UI default for L in one demo) made every SCEP CSR **without L** fail with **HTTP 500 "Internal error"** at PKIOperation. A CSR with `L=Chicago` was issued (2/2). The same template issued fine through the REST request API, which had sent `l=Chicago`. SCEP clients usually send CN only, so keep subject regexes at `.*` on SCEP end-entity templates. A policy `defaultValues` for L is harmless.
