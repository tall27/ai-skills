# NGTS glossary

- **TSG (Tenant Service Group):** SCM organizational scope with unique `tsg_id`; include it in OAuth token scope.
- **SCM service account:** IAM identity holding `client_id` and one-time-visible `client_secret`; assigned roles grant API access.
- **NGTS Built-in Account:** NGTS machine/API identity managed through `/v1/serviceaccounts`. It is not SCM IAM service account.
- **Certificate issuing template:** Policy-backed definition used to request/issue certificates.
- **Distributed issuer:** NGTS configuration combining sub-CA provider and workload issuance policies.
- **Sub-CA provider:** CA account/product configuration used by distributed issuer.
- **Machine identity / installation:** Binding between certificate and managed machine, with keystore/binding details.
- **Plugin:** Connector definition used to communicate with managed machine/integration.
- **VSatellite:** NGTS edge runtime for private-network access. Generated pairing/recovery codes and encryption-key operations are sensitive.
- **CMS:** Credential Management Service configuration, including CyberArk or HashiCorp backends.
