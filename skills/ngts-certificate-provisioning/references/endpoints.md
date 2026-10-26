# Certificate provisioning endpoints

Base URL: `https://api.strata.paloaltonetworks.com/ngts`. Do not log private-key material. Read `../../_shared/conventions.md`.

## Certificate Import

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| POST | `/outagedetection/v1/certificates` | Import raw certificate material | Base64 PEM content without delimiters; optional issuer chain | `CertificateImportResponse1` (`201`) |

## Private Key Import

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| POST | `/v1/certificates/imports` | Import certificate/private-key pair | `CertificateImportRequest2` | `CertificateImportResponse2` (`201`) |
| GET | `/v1/certificates/imports/{id}` | Get private-key import status | Path import UUID `id` | `CertificateImportStatusDetailResponse` |

## Certificate Requests

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| GET | `/outagedetection/v1/certificaterequests` | List requests | None | `CertificateRequestResponse` |
| POST | `/outagedetection/v1/certificaterequests` | Create request | `applicationId`, `certificateIssuingTemplateId`; optional `existingCertificateId`, `isVaaSGenerated`, CSR fields, ISO-8601 `validityPeriod` | `CertificateRequestResponse` (`201`) |
| GET | `/outagedetection/v1/certificaterequests/{id}` | Get request | Path request UUID `id` | `CertificateRequestInformation2` |
| POST | `/outagedetection/v1/certificaterequests/{id}/resubmission` | Resubmit request | Path `id`; `CertificateRequestResubmissionRequest` | `CertificateRequestResponse` |
| POST | `/outagedetection/v1/certificaterequests/validation` | Validate request before submit | `CertificateRequestRequest` | `CertificationRequestInformation` (`201`) |
| POST | `/outagedetection/v1/certificaterequestssearch` | Search requests | `Filter` | `CertificateRequestDocumentResponse` |

Key request fields: `applicationId`, `certificateIssuingTemplateId`, `certificateSigningRequest`, `isVaaSGenerated`, `csrAttributes`, `customAttributes`, `validityPeriod`, `tags`.

Key request-result fields: `id`, `status`, `subjectDN`, `certificateIds`, `product`, `keyType`, `keyLength`, `keyCurve`, `validityPeriod`.

Source: [NGTS OpenAPI](https://raw.githubusercontent.com/PaloAltoNetworks/pan.dev/master/openapi-specs/scm/config/ngts/tlsprotect-cloud.json).
