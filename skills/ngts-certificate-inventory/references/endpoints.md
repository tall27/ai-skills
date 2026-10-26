# Certificate inventory endpoints

Base URL: `https://api.strata.paloaltonetworks.com/ngts`. Use bearer auth and safety rules from `../../_shared/conventions.md`.

## Certificates

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/outagedetection/v1/certificates` | List certificates | Query: `ownershipTree`, `excludeSupersededInstances`, `subject`, `limit` | `CertificateResponse` |
| GET | `/outagedetection/v1/certificates/{id}` | Get certificate | Path `id`; query ownership/instance flags | `ExtendedCertificateInformation` |
| GET | `/outagedetection/v1/certificates/{id}/contents` | Download certificate contents | Path `id`; query `format`, `chainOrder`; `Accept` header | Certificate content |
| POST | `/outagedetection/v1/certificates/validation` | Validate certificates | `CertificateValidationRequest` | `CertificateValidationResponse` |
| POST | `/outagedetection/v1/certificates/retirement` | Retire certificates | `CertificateRetirementRequest` | `CertificateResponse` |
| POST | `/outagedetection/v1/certificates/recovery` | Recover retired certificates | `CertificateRecoveryRequest` | `CertificateResponse` |
| POST | `/outagedetection/v1/certificates/deletion` | Permanently delete retired certificates | `CertificateDeletionRequest` | `204` |
| POST | `/outagedetection/v1/certificatesearch` | Search certificates | `Filter`; ownership/instance query flags | `CertificateResponse` |

Key certificate fields: `id`, `certificateName`, `certificateStatus`, `fingerprint`, `issuerDN`, `issuerCN`, `issuerCertificateIds`, `applicationIds`, `instances`, `certificateAuthorityAccountId`, `certificateRequestId`, `encryptionType`, `extendedKeyUsage`.

## TLS Server Endpoints

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/outagedetection/v1/certificateinstances` | List certificate instances | Query `source`, `ipAddress`, `hostname`, `limit` | `ExtendedCertificateInstanceResponse` |
| GET | `/outagedetection/v1/certificateinstances/{id}` | Get certificate instance | Path `id` | `ExtendedCertificateInstanceInformation` |
| POST | `/outagedetection/v1/certificateinstances/validation` | Validate instances | `CertificateInstanceValidationRequest` | `Response` |
| POST | `/outagedetection/v1/certificateinstancesearch` | Search instances | `Filter` | `ExtendedCertificateInstanceResponse` |

Key instance fields: `certificateInstanceId`, `certificateId`, `hostname`, `ipAddress`, `port`, `sslProtocols`, `sslValidationStatus`, `deploymentStatus`, `serviceIds`.

## Certificate Discovery

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/integrationservices` | List integration services | Query `totalCount`, `edgeInstanceId` | `IntegrationServiceDetailsResponse` |
| POST | `/v1/integrationservices` | Create service | `IntegrationServiceCreationRequest` | `IntegrationServiceInformation` |
| GET | `/v1/integrationservices/{id}` | Get service | Path `id` | `IntegrationServiceInformation` |
| PATCH | `/v1/integrationservices/{id}` | Update service | Path `id`; `IntegrationServiceUpdateRequest` | `IntegrationServiceInformation` |
| DELETE | `/v1/integrationservices/{id}` | Delete service | Path `id`; query `retireCertificates` | `204` |

## Certificate Inventory Monitoring

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/outagedetection/v1/inventorymonitoringconfig/{type}` | Get monitoring config | Path `type` | `InventoryMonitoringConfigurationResponse` |
| PUT | `/outagedetection/v1/inventorymonitoringconfig/{type}` | Update monitoring config | Path `type`; `InventoryMonitoringConfigRequest` | `InventoryMonitoringConfigurationResponse` |
| PUT | `/outagedetection/v1/inventorymonitoringconfig/{type}/scheduler` | Update scheduler | Path `type`; query `runNow` | `InventoryMonitoringSchedulerInformation` |
| GET | `/v1/expirationnotifications/tenantconfiguration` | Get expiry notification config | None | `TenantExpirationNotificationConfiguration` |
| PUT | `/v1/expirationnotifications/tenantconfiguration` | Update expiry notification config | `TenantExpirationNotificationConfiguration` | same |

## Certificate Auto-renewal Monitoring

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/autorenewal/status` | Get renewal status | None | `StatusResponse` |
| GET | `/v1/autorenewal/tenantconfiguration` | Get renewal config | None | `TenantRenewalConfiguration` |
| PUT | `/v1/autorenewal/tenantconfiguration` | Update renewal config | `TenantRenewalConfiguration` | same |
| POST | `/v1/autorenewal/trigger` | Trigger renewal attempt | None | `StatusResponse` |

`TenantRenewalConfiguration` includes `id`, `defaultIssuingTemplateId`, `renewalWindow`, and `renewalActions`.

## Certificate Tags

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/tags` | List tags | None | `TagResponse` |
| POST | `/v1/tags` | Create tag | `TagRequest` | `TagInformation` (`201`) |
| POST | `/v1/tags/creation` | Bulk create tags | `TagsBulkRequest` | `TagsAndValuesResponse` (`201`) |
| POST | `/v1/tags/deletion` | Bulk delete tags | `TagsBulkRequest` | `202` |
| GET | `/v1/tags/values` | List all tag values | None | `TagValuesResponse` |
| GET | `/v1/tags/{name}` | Get tag | Path `name` | `TagInformation` |
| DELETE | `/v1/tags/{name}` | Delete tag | Path `name` | `202` |
| GET | `/v1/tags/{name}/values` | List tag values | Path `name` | `TagValuesResponse` |
| POST | `/v1/tags/{name}/values` | Create tag values | Path `name`; `TagValuesRequest` | `TagValuesResponse` (`201`) |
| DELETE | `/v1/tags/{name}/values/{value}` | Delete tag value | Path `name`, `value` | `202` |
| PATCH | `/v1/tagsassignment` | Add, replace, or delete entity tags | `TagsAssignRequest` | `TagsAssignResponse` |
| POST | `/v1/tagsassignment/aggregates` | Get bulk assignment counts | `TagsAssignmentAggregatesRequest` | `TagsAssignmentAggregatesResponse` |

`TagInformation`: `id`, `key`, `name`, `isReserved`.

Source: [NGTS OpenAPI](https://raw.githubusercontent.com/PaloAltoNetworks/pan.dev/master/openapi-specs/scm/config/ngts/tlsprotect-cloud.json).
