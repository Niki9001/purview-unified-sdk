# Microsoft Purview Unified Catalog Python SDK
The Microsoft Purview Unified Catalog Python SDK provides a Pythonic interface for interacting with Microsoft Purview Unified Catalog APIs. It simplifies authentication and common operations, allowing developers to manage governance resources through an intuitive object-oriented API. 
Based on Microsoft Purview API Version 2026-03-20-preview

## Features

- Business Domains
- Data Products
- Data Assets
- Data Columns
- Glossary Terms
- Objectives
- Key Results
- Relationships
- Authentication
- Automatic pagination

## Installation

```bash
pip install purview-unified-sdk

Verify the installation:

```python
from purview import PurviewClient, PurviewConfig

print(PurviewClient)
```

---

# Prerequisites

Before using the SDK, ensure you have:

- Python 3.10 or later
- Access to Microsoft Purview Unified Catalog
- A Microsoft Entra ID tenant
- Appropriate permissions to access Purview APIs

---

# Authentication

The SDK authenticates users through Microsoft Entra ID (formerly Azure Active Directory).

Authentication requires two pieces of information:

- **Tenant ID**
- **Username**

The SDK will use your Microsoft account to acquire an access token for Microsoft Purview.

---

## Tenant ID

The Tenant ID identifies your Microsoft Entra organization.

It is typically a GUID, for example:

```text
12345678-1234-1234-1234-123456789abc
```

You can obtain the Tenant ID from:

- Azure Portal → Microsoft Entra ID → Overview
- Your organization's Azure administrator

---

## Username

The username should be the Microsoft account used to access Microsoft Purview.

For most enterprise users, this is your corporate email address, for example:

```text
john.smith@contoso.com
```

Some organizations may use a User Principal Name (UPN) that is different from the user's email address. In that case, use the UPN assigned by your Microsoft Entra administrator.

---

## Example

```python
import os

from purview import PurviewClient, PurviewConfig

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:

    domains = client.domains.list_all()
```

---

## Environment Variables

The SDK recommends storing credentials in environment variables.

Example:

```text
PURVIEW_TENANT_ID=12345678-1234-1234-1234-123456789abc
PURVIEW_USERNAME=john.smith@contoso.com
PURVIEW_DATA_PRODUCT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PURVIEW_DATA_ASSET_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PURVIEW_GLOSSARY_TERM_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PURVIEW_DATA_PRODUCT_OWNER_ID = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PURVIEW_DOMAIN_ID = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---
## Token Caching

By default, the SDK does not configure a persistent authentication token cache.

As a result, depending on the authentication flow, you may be prompted to sign in again when starting a new application session.

For production applications, configuring a persistent token cache is recommended to reduce repeated authentication prompts and improve the user experience.

The Microsoft Authentication Library provides several options for implementing persistent token caching. One common approach is to use the `msal-extensions` package.

Example:

```python
import msal
from msal_extensions import (
    FilePersistence,
    PersistedTokenCache,
)

persistence = FilePersistence("token_cache.bin")
cache = PersistedTokenCache(persistence)

app = msal.PublicClientApplication(
    client_id=CLIENT_ID,
    authority=AUTHORITY,
    token_cache=cache,
)
```

The SDK can then be configured to use the `PublicClientApplication` instance or its token cache, depending on your application's authentication architecture.
```
---
## First-Time Authentication

The first time the SDK is used, you may be prompted to sign in to your Microsoft account.

After successful authentication, the authentication token is securely cached by the Microsoft Authentication Library (MSAL). Future SDK sessions can typically reuse the cached token without requiring you to sign in again until the token expires or is revoked.

---

## Multi-Tenant Organizations

If your Microsoft account belongs to multiple organizations (tenants), ensure that the Tenant ID supplied to the SDK matches the Microsoft Purview instance you intend to access.

Using an incorrect Tenant ID may result in authentication failures or authorization errors.

---

## Common Authentication Errors

### Invalid Tenant ID

Verify that the Tenant ID is correct and that your account belongs to the specified Microsoft Entra tenant.

### Invalid Username

Verify that the username matches the Microsoft account (typically your corporate email or assigned UPN) used to access Microsoft Purview.

### Permission Denied

Authentication may succeed even if authorization fails.

Ensure that your account has the required Microsoft Purview permissions for the requested operation.

## Using environment variables

```python
import os

from purview import PurviewClient, PurviewConfig

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:
    ...
```

---

# SDK Architecture

The SDK uses a single entry point:

```python
client = PurviewClient(...)
```

Each resource is exposed as a dedicated client.

| Resource | Client |
|----------|--------|
| Business Domains | `client.domains` |
| Data Products | `client.data_products` |
| Data Assets | `client.data_assets` |
| Glossary Terms | `client.glossary_terms` |
| Relationships | `client.relationships` |
| Policies | `client.policies` |
| Objectives | `client.objectives` |
| Key Results | `client.key_results` |
| Data Quality | `client.data_quality` |

---

# Quick Start

Retrieve all Business Domains.

```python
from purview import PurviewClient, PurviewConfig

config = PurviewConfig(
    tenant_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

with PurviewClient(
    config,
    username="user@company.com",
) as client:

    domains = client.domains.list_all()

for domain in domains:
    print(domain.name)
```

---

# Supported Resources

The SDK currently supports:

## Business Domains

Typical operations:

- Create
- Retrieve
- List
- Update
- Delete

---

## Data Products

Typical operations:

- Create
- Retrieve
- List
- Update
- Delete

---

## Data Assets

Typical operations:

- Retrieve
- List
- Update relationships

---

## Glossary Terms

Typical operations:

- Create
- Retrieve
- List
- Update
- Delete

---

## Relationships

Manage relationships between supported Purview resources.

Examples include:

- Data Product ↔ Business Domain
- Data Product ↔ Objective
- Objective ↔ Key Result
- Data Asset ↔ Data Product
- Glossary Term ↔ Data Asset

---

## Policies

Supported operations include:

- List policies
- Retrieve policy details

---

## Objectives

Typical operations:

- Create
- Retrieve
- List
- Update
- Delete

---

## Key Results

Typical operations:

- Create
- Retrieve
- List
- Update
- Delete

---

## Data Quality

Data Quality APIs supported by the SDK.

---

# Examples

Example scripts are included with the SDK.

They demonstrate common scenarios, including:

- Creating Business Domains
- Managing Data Products
- Updating Data Assets
- Creating Glossary Terms
- Managing Relationships
- Working with Objectives
- Working with Key Results
- Listing Policies
- Data Quality operations

---

# Error Handling

It is recommended to wrap SDK calls in exception handling.

```python
try:
    ...
except Exception as e:
    print(e)
```

---

# Best Practices

- Use `PurviewClient` as a context manager.
- Store credentials in environment variables.
- Avoid hardcoding resource IDs in production code.
- Reuse the same client instance whenever possible.

---

# Troubleshooting

## ModuleNotFoundError

Ensure the SDK is installed correctly.

```bash
pip install purview-unified-sdk
```

---

## Authentication failed

Verify:

- Tenant ID
- Username
- Microsoft account access
- Network connectivity
- Required Purview permissions

---

## Permission denied

Ensure your account has sufficient permissions to perform the requested operation.

---

# API Reference

Refer to the SDK documentation and example scripts for detailed usage of each resource and operation.

---

# License

This project is licensed under the applicable project license.
