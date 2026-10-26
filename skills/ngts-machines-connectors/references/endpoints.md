# NGTS machines and connector endpoints

Base URL: `https://api.strata.paloaltonetworks.com/ngts`. Read `../../_shared/conventions.md`. Do not emit secret values, pairing/recovery codes, or encryption-key material.

## Machines

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/machines` | List machines | None | `MachinesResponse` |
| POST | `/v1/machines` | Create machine | `MachineCreationRequest` | `MachineInformation` (`201`) |
| GET | `/v1/machines/{id}` | Get machine | Path UUID `id` | `MachineInformation` |
| PATCH | `/v1/machines/{id}` | Update machine | Path `id`; machine update request | `MachineInformation` |
| DELETE | `/v1/machines/{id}` | Delete machine | Path `id` | `204` |
| GET | `/v1/machines/{id}/discovery` | Get machine discovery | Path `id` | `MachineDiscoveryResultInformation` |
| POST | `/v1/machines/{id}/discovery/abort` | Abort discovery | Path `id` | `MachineInformation` (`202`) |
| POST | `/v1/machines/{id}/batchprovisionings/abort` | Abort batch provisioning | Path `id` | `202` |
| POST | `/v1/machines/{id}/workflows` | Start machine workflow | Path `id`; workflow request | `MachineInformation` (`201`) |
| POST | `/v1/machinesearch` | Search machines | Machine search expression | `MachineDocumentResponse` |

`MachineCreationRequest` has required `name`, `pluginId`, `connectionDetails`; optional `machineTypeId`, `owningTeamId`, `tags`. Machine result adds `status`, `discoveryStatus`, `batchProvisioningStatus`, `edgeInstanceId`.

## Machine Types

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/machinetypes` | List deprecated machine types | None | Generic object |

Use plugin catalog for current connector capability where applicable.

## Machine Installations

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/machineidentities` | List machine identities | None | `MachineIdentityResponse` |
| POST | `/v1/machineidentities` | Create identity/installation | `MachineIdentityCreationRequest` | `MachineIdentityInformation` (`201`) |
| GET | `/v1/machineidentities/{id}` | Get identity | Path UUID `id` | `MachineIdentityInformation` |
| PATCH | `/v1/machineidentities/{id}` | Update identity | Path `id`; `MachineIdentityUpdateRequest` | `MachineIdentityInformation` |
| DELETE | `/v1/machineidentities/{id}` | Delete identity | Path `id` | `204` |
| POST | `/v1/machineidentities/{id}/workflows` | Start identity workflow | Path `id`; `MachineIdentityWorkflowRequest` | `MachineIdentityWorkflowInformation` (`201`) |
| POST | `/v1/machineidentitysearch` | Search identities | `MachineIdentitySearchRequest` | `MachineIdentityDocumentResponse` |

Create fields: required `certificateId`, `machineId`; plus `binding`, `keystore`. Result includes `status`, `lastSeenOn`.

## Plugins (Connectors)

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/plugins` | List plugins | Query `pluginTypes`, `includeDisabled` | Plugin collection |
| POST | `/v1/plugins` | Create local plugin | `PublicPluginCreationRequest` | `PluginResponse` (`201`) |
| GET | `/v1/plugins/{id}` | Get plugin | Path `id` | `Plugin` |
| PATCH | `/v1/plugins/{id}` | Update local plugin | Path `id`; `PublicPluginUpdateRequest` | Success (`200`) |
| DELETE | `/v1/plugins/{id}` | Delete local plugin | Path `id` | `204` |
| POST | `/v1/plugins/{id}/disablements` | Disable plugin | Path `id` | `PluginResponse` (`201`) |
| DELETE | `/v1/plugins/{id}/disablements` | Remove disablement | Path `id` | `204` |
| GET | `/v1/plugins/disablements` | List disabled plugins | None | `PluginResponse` |

Plugin fields: `id`, `name`, `pluginType`, `manifest`, `workTypes`, `revision`, `maintainer`, `disabled`.

## Credential Management

### Credential Management Service configurations

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/credentialmanagerconfigurations` | List CMS configurations | CMS-type query | `200GetCMSConfigurations` |
| POST | `/v1/credentialmanagerconfigurations` | Create CMS configuration | `CreateCMSConfigurationsBodyRequest` | `201CreateCMSConfigurations` |
| PUT | `/v1/credentialmanagerconfigurations` | Update CMS configuration | `UpdateCMSConfigurationsBodyRequest` | `200UpdateCMSConfiguration` |
| GET | `/v1/credentialmanagerconfigurations/{id}` | Get CMS configuration | Path `id` | `200GetCMSConfiguration` |
| DELETE | `/v1/credentialmanagerconfigurations/{id}` | Delete CMS configuration | Path `id` | `204` |
| POST | `/v1/credentialmanagerconfigurations/test` | Test proposed CMS connection | `TestCMSConfigurationBodyRequest` | `200TestCMSConfiguration` |
| POST | `/v1/credentialmanagerconfigurations/{id}/test` | Test stored CMS connection | Path `id` | `200TestCMSConfiguration` |

Supports CyberArk and HashiCorp configuration schemas. CMS result fields include `id`, `name`, `cmsType`, `cmsDetails`, `consumerTsgIds`, `vSatelliteIds`, `shareWithAll`.

### Shared credentials

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/credentials` | List shared credentials | Detail/CMS-type/credential-ID/team-ID/auth-type query filters | `200GetCredentials` |
| POST | `/v1/credentials` | Create shared credential | `AddCredentialsBodyRequest` | `201AddCredentials` |
| PUT | `/v1/credentials` | Update shared credential | `UpdateCredentialBodyRequest` | `200UpdateCredential` |
| DELETE | `/v1/credentials` | Bulk delete credentials | Query credential `ids` | `200DeleteCredentials` |
| GET | `/v1/credentials/{id}` | Get credential metadata/detail | Path UUID `id`; optional detail flag | `200GetCredential` |
| DELETE | `/v1/credentials/{id}` | Delete credential | Path `id` | `204` |
| POST | `/v1/credentials/test` | Test stored/supplied credential | `TestCredentialBodyRequest` | `200TestCredential` |

## VSatellite

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| POST | `/v1/edgeinstances/{id}/update` | Trigger Satellite update | Path Satellite ID `id` | `202` |
| GET | `/v1/edgeencryptionkeys` | List Satellite encryption keys | Query `edgeInstanceId` | `EncryptionKeysResponse` |
| GET | `/v1/edgeencryptionkeys/{id}` | Get Satellite encryption key | Path `id` | `EncryptionKeyInformation` |
| GET | `/v1/edgeinstances` | List Satellite instances | Query `environmentId` | `EdgeInstanceResponse` |
| GET | `/v1/edgeinstances/{id}` | Get Satellite instance | Path `id`; query `statusDetails` | `EdgeInstanceInformation` |
| PUT | `/v1/edgeinstances/{id}` | Update Satellite instance | Path `id`; `EdgeInstanceRequest` | `EdgeInstanceInformation` |
| DELETE | `/v1/edgeinstances/{id}` | Delete (deregister) Satellite instance | Path `id` | `204` |
| POST | `/v1/pairingcodes/satellite` | Create pairing code | `PairingCodeRequest` | `PairingCodeInformation` (`201`) |
| POST | `/v1/recoverycodes/satellite` | Create recovery code | `RecoveryCodeRequest` | `RecoveryCodeInformation` (`201`) |
| GET | `/v1/edgeworkers` | List Satellite workers | Query `edgeInstanceId` | `EdgeWorkersResponse` |
| POST | `/v1/edgeworkers` | Create Satellite worker | `EdgeWorkerRequest` | `EdgeWorkerInformation` (`201`) |
| POST | `/v1/edgeworkers/{id}/pair` | Pair worker with Satellite | Path worker ID `id`; `EdgeWorkerRequest` | `EdgeWorkerInformation` |
| DELETE | `/v1/edgeworkers/{id}` | Delete Satellite worker | Path worker ID `id` | `204` |
| GET | `/v1/updatesconfig` | Get update configuration | None | `UpdatesConfigResponse` |
| PATCH | `/v1/updatesconfig` | Create/update update configuration | `UpdatesConfigRequest` | `UpdatesConfigResponse` |

`EdgeInstanceInformation` fields: `id`, `name`, `edgeStatus`, `edgeType`, `kubernetesVersion`, `satelliteVersion`, `upgradeStatus`, `statusDetails`, `integrationServicesCount`.

`edgeStatus` values seen live: `REGISTERED` (paired, no satellite reporting yet — `satelliteVersion` null),
`ACTIVE`, `LOST_CONNECTION` (host gone; survives `delete-stack` and must be removed via the
API or UI). `DELETE /v1/edgeinstances/{id}` is **not in the published OpenAPI table** but works
and returns `204` — verified 2026-10-05 against a lab TSG, where it cleared 8
`LOST_CONNECTION` hubs with `integrationServicesCount: 0`. Filter on
`edgeStatus == "LOST_CONNECTION"` server-side-list then client-side, since the endpoint takes
only `environmentId`. Delete attached workers (`GET /v1/edgeworkers?edgeInstanceId=`) first.

Source: [NGTS OpenAPI](https://raw.githubusercontent.com/PaloAltoNetworks/pan.dev/master/openapi-specs/scm/config/ngts/tlsprotect-cloud.json).
