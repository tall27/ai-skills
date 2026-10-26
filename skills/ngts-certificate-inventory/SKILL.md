---
name: ngts-certificate-inventory
description: Find, inspect, download, validate, tag, discover, retire, recover, monitor, or configure renewal for certificates and TLS endpoints already known to NGTS. Do not use to import certificate material, request new certificates, or approve requests.
---

# NGTS certificate inventory

Read `../_shared/conventions.md` first.

## Scope

Certificates, TLS certificate instances, discovery integrations, inventory/expiration monitoring, auto-renewal, and tags.

**Boundary:** Use `ngts-certificate-provisioning` to import/request certificates. Use `ngts-certificate-governance` for issuance/revocation approval rules.

## Workflows

### Investigate certificate exposure

1. Search certificates or certificate instances with server-side search/filter.
2. Inspect selected certificate and associated instances.
3. Validate only intended certificate/instance IDs.
4. Check discovery, expiration, and auto-renewal configuration before changing service state.

### Retire or delete certificate

1. Get certificate and confirm IDs, status, instance impact, and replacement coverage.
2. Retire first; verify outcome.
3. Delete only retired, confirmed targets. Recovery applies to retired items.

### Configure discovery or monitoring

1. List existing integration/configuration.
2. Update one config with validated payload.
3. Re-read config/status. Trigger auto-renewal only after confirming scope.

Full operations: `references/endpoints.md`.
