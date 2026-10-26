# Certificate governance endpoints

Base URL: `https://api.strata.paloaltonetworks.com/ngts`. Read `../../_shared/conventions.md`.

## Certificate Request Approvals

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| POST | `/v1/certificaterequests/{id}/approval/{decision}` | Approve/reject pending request | Path request UUID `id`, `decision` (`approve`/`reject`); `ApprovalDecisionRequest` with `reason` | `CertificateRequestInformation1` |
| POST | `/v1/certificaterequests/approval/bulk/{decision}` | Bulk approve/reject | Path `decision`; `BulkApprovalRequest`: `ids`, `reason`, `wsClientId` | `BulkApprovalResponse` (`201`) |
| POST | `/v1/certificaterequests/approvalrules` | Create request approval rule | `CertificateRequestApprovalRulesRequest` | `CertificateRequestApprovalRuleOpenApi` (`201`) |
| GET | `/v1/certificaterequests/approvalrules` | List request approval rules | None | `CertificateRequestApprovalRulesResponseOpenApi` |
| GET | `/v1/certificaterequests/approvalrules/{id}` | Get request approval rule | Path UUID `id` | `CertificateRequestApprovalRuleOpenApi` |
| PUT | `/v1/certificaterequests/approvalrules/{id}` | Update request approval rule | Path `id`; `CertificateRequestApprovalRulesUpdateRequest` | `CertificateRequestApprovalRuleOpenApi` |
| DELETE | `/v1/certificaterequests/approvalrules/{id}` | Delete request approval rule | Path `id` | `CertificateRequestApprovalRuleDeleteResponseOpenApi` |
| GET | `/v1/certificaterequests/approvalrequests/{entityId}` | Get approval request for entity | Path entity UUID `entityId` | `ApprovalRequestInformation` |

Request approval-rule fields include `name`, `type`, `approvers`, `atLeast`, `autoApproveOnRenew`, `autoRejectionThreshold`, `finalApprover`, `priority`, `conditions`, `exceptions`, and `continueProcessingOnException`.

## Certificate Revocation Approval Rules

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| POST | `/v1/certificates/revocations/approvalrules` | Create revocation rule | `CertificateRevocationApprovalRulesRequest` | `CertificateRevocationApprovalRuleOpenApi` (`201`) |
| GET | `/v1/certificates/revocations/approvalrules` | List revocation rules | None | `CertificateRevocationApprovalRulesResponseOpenApi` |
| GET | `/v1/certificates/revocations/approvalrules/{id}` | Get revocation rule | Path UUID `id` | `CertificateRevocationApprovalRuleOpenApi` |
| PUT | `/v1/certificates/revocations/approvalrules/{id}` | Update revocation rule | Path `id`; `CertificateRevocationApprovalRulesUpdateRequest` | `CertificateRevocationApprovalRuleOpenApi` |
| DELETE | `/v1/certificates/revocations/approvalrules/{id}` | Delete revocation rule | Path `id` | `CertificateRevocationApprovalRuleDeleteResponseOpenApi` |

Revocation-rule fields include `name`, `type`, `approvers`, `atLeast`, `autoRejectionThreshold`, `finalApprover`, `priority`, `conditions`, `exceptions`, and `continueProcessingOnException`.

## Certificate Issuing Templates

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/certificateissuingtemplates` | List templates | Query `certificateAuthorityAccountId` | `CertificateIssuingTemplateResponse` |
| POST | `/v1/certificateissuingtemplates` | Create template | `CertificateIssuingTemplateRequest` | `CertificateIssuingTemplateResponse` (`201`) |
| GET | `/v1/certificateissuingtemplates/{id}` | Get template | Path UUID `id` | `CertificateIssuingTemplateInformation` |
| PUT | `/v1/certificateissuingtemplates/{id}` | Replace template | Path `id`; `CertificateIssuingTemplateRequest` | `CertificateIssuingTemplateInformation` (`200`/`202`) |
| DELETE | `/v1/certificateissuingtemplates/{id}` | Delete template | Path `id` | `204` |
| POST | `/v1/certificateissuingtemplates/domainssynchronization` | Synchronize CA domain lists | `IssuingTemplatesDomainsSyncRequest` | `IssuingTemplateDomainsSyncResponse` |

Template fields include `id`, `name`, `certificateAuthority`, `certificateAuthorityProductOptionId`, `keyTypes`, `keyReuse`, `csrUploadAllowed`, `recommendedSettings`, sharing fields, and SAN regex fields.

## Workload Issuance Policies

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/distributedissuers/policies` | List policies | None | `PolicyResponse` |
| POST | `/v1/distributedissuers/policies` | Create policy | Policy creation request | `ExtendedPolicyInformation` (`201`) |
| GET | `/v1/distributedissuers/policies/{id}` | Get policy | Path `id` | `ExtendedPolicyInformation` |
| PATCH | `/v1/distributedissuers/policies/{id}` | Update policy | Path `id`; policy update request | `ExtendedPolicyInformation` |
| DELETE | `/v1/distributedissuers/policies/{id}` | Delete policy | Path `id` | `PolicyDeleteResponse` |

Policy fields: `id`, `name`, `keyAlgorithm`, `keyUsages`, `extendedKeyUsages`, `sans`, `subject`, `validityPeriod`, `shareWithAll`.

Source: [NGTS OpenAPI](https://raw.githubusercontent.com/PaloAltoNetworks/pan.dev/master/openapi-specs/scm/config/ngts/tlsprotect-cloud.json).
