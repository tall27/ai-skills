# NGTS issuer endpoints

Base URL: `https://api.strata.paloaltonetworks.com/ngts`. Read `../../_shared/conventions.md` and `../../_shared/glossary.md`.

## Issuer Configurations

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/distributedissuers/configurations` | List distributed issuer configurations | None | `ConfigurationResponse` |
| POST | `/v1/distributedissuers/configurations` | Create configuration | Configuration create request: required `name`, `subCaProviderId`, `policyIds` | `ExtendedConfigurationInformation` (`201`) |
| GET | `/v1/distributedissuers/configurations/{id}` | Get configuration | Path `id` | `ExtendedConfigurationInformation` |
| PATCH | `/v1/distributedissuers/configurations/{id}` | Update configuration | Path `id`; configuration update request | `ExtendedConfigurationInformation` |
| DELETE | `/v1/distributedissuers/configurations/{id}` | Delete configuration | Path `id` | `ConfigurationDeleteResponse` |

Key fields: `id`, `name`, `subTsgId`, `minTlsVersion`, `policyIds`, `controllerAllowedPolicyIds`, `unixSocketAllowedPolicyIds`, `serviceAccountIds`, `clientAuthentication`, `clientAuthorization`, `cloudProviders`, `advancedSettings`, and short/long/ultra-short-lived certificate counts.

## Issuer Sub-CA Providers

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/distributedissuers/subcaproviders` | List providers | None | `SubCaProviderResponse` |
| POST | `/v1/distributedissuers/subcaproviders` | Create provider | Sub-CA provider create request | `SubCaProviderInformation` (`201`) |
| GET | `/v1/distributedissuers/subcaproviders/{id}` | Get provider | Path `id` | `SubCaProviderInformation` |
| PATCH | `/v1/distributedissuers/subcaproviders/{id}` | Update provider | Path `id`; provider update request | `SubCaProviderInformation` |
| DELETE | `/v1/distributedissuers/subcaproviders/{id}` | Delete provider | Path `id` | `SubCaProviderDeleteResponse` |

Key fields: `id`, `name`, `caType`, `caAccountId`, `caProductOptionId`, `commonName`, `keyAlgorithm`, ISO-8601 `validityPeriod`, `pkcs11`, `shareWithAll`, `sharedWithSubTsgIds`.

## Issuer Certificates

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/v1/distributedissuers/intermediatecertificates` | List intermediate certificates | None | Intermediate certificate collection |

Key fields: `id`, `commonName`, PEM `certificate`, `issuerCertificates`, back-reference `configuration`, `status`, `validityStart`, `validityEnd`, and certificate counts.

Source: [NGTS OpenAPI](https://raw.githubusercontent.com/PaloAltoNetworks/pan.dev/master/openapi-specs/scm/config/ngts/tlsprotect-cloud.json).
