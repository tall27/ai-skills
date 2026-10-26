---
name: ngts-platform-ops
description: Search, filter, inspect, or export NGTS activity and audit event logs. Do not use for certificate inventory changes, authentication setup, or connector administration.
---

# NGTS platform operations

Read `../_shared/conventions.md` first.

## Scope

Activity-log search, export, and activity-type catalog.

## Workflow

1. Get activity types when building filters.
2. Use narrow date, tenant, activity, or severity criteria in activity-log filter.
3. Search before export to validate result scope.
4. Treat exported logs as sensitive operational data; use approved storage and avoid sharing payload fields broadly.

Full operations: `references/endpoints.md`.
