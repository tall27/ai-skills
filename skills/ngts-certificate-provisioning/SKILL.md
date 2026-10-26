---
name: ngts-certificate-provisioning
description: Import existing certificate or private-key material into NGTS; create, validate, inspect, search, or resubmit certificate requests; create, inspect, or deactivate SCEP servers and diagnose SCEP enrollment. Do not use for monitoring existing inventory, policy/approval rules, or CA issuer configuration.
---

# NGTS certificate provisioning

Read `../_shared/conventions.md` first.

## Scope

Certificate import, private-key import jobs, certificate request lifecycle.

**Boundary:** `ngts-certificate-inventory` handles existing inventory. `ngts-certificate-governance` owns issuing templates and approval workflows. `ngts-issuers` owns CA connectivity.

## Workflows

### Import certificate material

1. Confirm ownership, certificate chain, and target tenant.
2. Use certificate import for raw certificate material; use private-key import only when private key handling is authorized.
3. Never expose PEM/private key values in logs or chat.
4. Inspect import result/status and verify certificate appears in inventory.

### Request certificate

1. Get issuing template ID from governance skill.
2. Validate request payload before create.
3. Submit request, then get/search request until status is terminal.
4. Use resubmission only for documented failed/rework flow.

Full operations: `references/endpoints.md`.

## SCEP servers

Feature check, create (Static challenge returned once), read template links, deactivate = delete, enrollment failure diagnosis: `references/scep-servers.md` (GraphQL, verified live).
