# Authentication

The Purview Unified SDK supports multiple Microsoft Entra ID authentication methods through the Azure Identity library.

Choose the authentication method that best matches your application scenario.

---

## Supported Authentication Methods

| Authentication Method | Typical Scenario |
|-----------------------|------------------|
| Interactive Browser | Local development and interactive applications (SSO) |
| Device Code | Remote terminals, SSH sessions, and environments without a browser |
| Client Secret | Service principals, automation, and CI/CD pipelines |
| Managed Identity | Azure-hosted applications |
| Default Azure Credential | Applications that should automatically select the best available credential |

---

## Interactive Browser Authentication

Interactive Browser Authentication is recommended for local development.

The SDK opens your default web browser and prompts you to sign in with your Microsoft account.

```python
from purview import PurviewClient, PurviewConfig

config = PurviewConfig(
    tenant_id="<tenant-id>",
)

with PurviewClient(
    config,
    username="user@company.com",
) as client:
    ...
```

The optional `username` parameter is used as a login hint and is typically your corporate email address or User Principal Name (UPN).

---

## Device Code Authentication

Device Code Authentication is useful when a web browser is unavailable, such as when working over SSH or on a remote server.

```python
from azure.identity import DeviceCodeCredential

credential = DeviceCodeCredential(
    tenant_id=tenant_id,
)

with PurviewClient(
    config,
    credential=credential,
) as client:
    ...
```

---

## Client Secret Authentication

Client Secret Authentication is recommended for service principals and unattended applications.

```python
from azure.identity import ClientSecretCredential

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
)

with PurviewClient(
    config,
    credential=credential,
) as client:
    ...
```

---

## Managed Identity Authentication

Managed Identity Authentication is recommended for applications running in Azure.

```python
from azure.identity import ManagedIdentityCredential

credential = ManagedIdentityCredential()

with PurviewClient(
    config,
    credential=credential,
) as client:
    ...
```

No secrets or passwords are required.

---

## Default Azure Credential Authentication

Default Azure Credential automatically selects the most appropriate authentication method for the current environment.

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential(
    tenant_id=tenant_id,
)

with PurviewClient(
    config,
    credential=credential,
) as client:
    ...
```

This option is recommended when developing applications that may run in multiple environments.

---

## Token Caching

Interactive Browser Authentication uses Azure Identity's persistent token cache.

After a successful sign-in, the SDK can typically reuse the cached authentication token until it expires or is revoked, reducing the need for repeated sign-in.

---

## Multi-Tenant Organizations

If your Microsoft account belongs to multiple Microsoft Entra ID tenants, ensure that the `tenant_id` supplied to `PurviewConfig` matches the Microsoft Purview environment you intend to access.

Using an incorrect tenant ID may result in authentication failures or authorization errors.

---

## Common Authentication Errors

### Invalid Tenant ID

Verify that the configured tenant ID matches your Microsoft Entra ID tenant.

---

### Invalid Username

When using Interactive Browser Authentication, ensure that the username (login hint) matches your Microsoft account, typically your corporate email address or UPN.

---

### Incorrect API Endpoint

The SDK is designed for Microsoft Purview Unified Catalog.

Using legacy Azure Purview endpoints may result in API errors such as:

- `404 Not Found`
- `Resource not found`
- `Unsupported API`

---

### Permission Denied

Authentication may succeed even if authorization fails.

Ensure that your Microsoft account or service principal has the required Microsoft Purview permissions.

---
!!! danger "Important"

    **One of the most common causes of `401 Unauthorized` and `403 Forbidden` errors is using a classic Microsoft Purview Data Catalog endpoint instead of a Microsoft Purview Unified Catalog endpoint.**

    The Purview Unified SDK is designed to work exclusively with the **Microsoft Purview Unified Catalog API**.

    If you receive authentication or authorization errors, first verify that your application is using a **Unified Catalog endpoint**, not a classic Microsoft Purview Data Catalog endpoint.

---

## Next Steps

Continue with the **Quick Start** guide to create your first connection to Microsoft Purview Unified Catalog.

➡️ **Next:** [Configuration](configuration.md)