---
name: ngts-machines-connectors
description: Manage NGTS machines, machine types, certificate-to-machine installations, plugins/connectors, Credential Management Service settings, shared credentials, and VSatellite infrastructure. Do not use for certificate policy approval or inventory monitoring.
---

# NGTS machines and connectors

Read `../_shared/conventions.md` and `../_shared/glossary.md` first.

## Scope

Machines, machine identities/installations, plugin connectors, CMS/shared credentials, VSatellite instances/workers/keys/codes/update settings.

## Workflows

### Provision managed machine

1. List compatible plugins and machine types.
2. Create/get machine, then verify discovery/connection workflow state.
3. Create machine identity only after certificate ID and machine ID are confirmed.
4. Re-read installation status and `lastSeenOn` after workflow.

### Configure connector credentials

1. List CMS configuration and existing shared credential metadata.
2. Test connection before attaching credentials to production machines.
3. Do not expose secret values in payload output.
4. Confirm VSatellite reachability when test executes through edge infrastructure.

### Operate VSatellite

Pairing/recovery codes and encryption-key actions can change access to private-network operations. Get exact instance/worker state, confirm target, then mutate. Never output generated codes or key material.

### Remove stale VSatellites

`LOST_CONNECTION` satellites outlive both their EC2 host and their CloudFormation stack, so a
torn-down POV leaves its registration behind and that name then blocks re-launching with the
same `CustomerName`. Clean up with `GET /v1/edgeinstances`, filter `edgeStatus ==
"LOST_CONNECTION"` client-side (the endpoint only takes `environmentId`), confirm
`integrationServicesCount` is 0, delete any attached workers, then `DELETE
/v1/edgeinstances/{id}` → 204. Never touch `REGISTERED` or `ACTIVE` instances in the same pass.

Credentials come from the `NGTS_CLIENT_ID` / `NGTS_CLIENT_SECRET` / `NGTS_TSG_ID` environment
variables — check `NGTS_TSG_ID` against the tenant the user named before mutating anything.

Full operations: `references/endpoints.md`.
