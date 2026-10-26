---
name: ngts-certificate-governance
description: Create or manage certificate issuing templates, certificate request approvals, certificate revocation approval rules, and distributed workload issuance policies. Use for policy and human approval workflows, not certificate import or CA connector setup.
---

# NGTS certificate governance

Read `../_shared/conventions.md` first.

## Scope

Certificate issuing templates, certificate request approvals, certificate revocation approval rules, workload issuance policies.

**Boundary:** `ngts-certificate-provisioning` submits requests. `ngts-issuers` configures issuer/sub-CA plumbing. Use this skill for rules deciding what gets issued or approved.

## Workflows

### Change policy/template

1. Get existing object and identify dependent request/issuer flows.
2. Validate SAN, key, validity, approver, and sharing constraints.
3. Update/create policy or template.
4. Get object again and run non-production or limited-scope request validation.

### Approve or reject request

1. Get request and approval-request state.
2. Confirm decision, approver authorization, reason, and exact IDs.
3. Submit individual or bulk decision.
4. Re-read request status; do not assume issuance completed.

Full operations: `references/endpoints.md`.

## Built-in PKI issuance policies and request policies

GraphQL issuance policies + REST issuing templates ("request policies") bound to a Built-in PKI CA, the SCEP set of 3+3, and subject-regex pitfalls: `references/issuance-and-request-policies.md` (verified live).
