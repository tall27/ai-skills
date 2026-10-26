---
name: ngts-issuers
description: Configure or inspect NGTS distributed issuers, issuer sub-CA providers, issuer intermediate certificate chains, and Built-in PKI CA hierarchies (create/decommission root and sub-CAs through PKI proposed changes). Do not use for request approval rules, certificate imports, or machine connector operations.
---

# NGTS issuer configuration

Read `../_shared/conventions.md` and `../_shared/glossary.md` first.

## Scope

Distributed issuer configurations, sub-CA providers, intermediate/issuer certificate inventory.

**Boundary:** Workload issuance policies belong to `ngts-certificate-governance`, even though they share distributed-issuer URL family.

## Workflow

1. Inspect sub-CA provider and existing issuer configuration.
2. Confirm CA account/product, key algorithm, validity, sub-TSG sharing, policy IDs, and service-account IDs.
3. Create/update provider before dependent issuer configuration.
4. Inspect intermediate certificate status/chain after configuration change.
5. Do not delete provider/configuration until dependent issuer workloads are identified and migrated.

Full operations: `references/endpoints.md`.

## Built-in PKI CAs

Root/sub-CA creation, issuer → CA account link (`caOpsID`), provisioning-workflow lock, decommission cascade: `references/builtin-pki.md` (GraphQL only, verified live).
