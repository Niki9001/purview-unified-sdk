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

As a result, you may be prompted to sign in again when starting a new application session.

For production applications, configuring a persistent token cache is recommended to reduce repeated authentication prompts and improve the user experience.

The Microsoft Authentication Library (MSAL) supports persistent token caching through several mechanisms. One common approach is to use the `msal-extensions` package.

### Example

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

After a successful sign-in, the authentication token is securely stored in the persistent cache. Future application sessions can typically reuse the cached token until it expires or is revoked, reducing the need for repeated authentication.

---

## First-Time Authentication

The first time the SDK requires authentication, you will be prompted to sign in with your Microsoft account.

For most enterprise users, the Microsoft account is the corporate email address or User Principal Name (UPN) associated with the organization's Microsoft Entra ID tenant.

For example:

```text
john.smith@contoso.com
```

If a persistent token cache has been configured, future SDK sessions can typically reuse the cached authentication token without requiring you to sign in again until the token expires or is revoked.

If persistent token caching is not configured, you may be prompted to authenticate each time a new application session starts.

---

## Multi-Tenant Organizations

Some Microsoft accounts are associated with multiple Microsoft Entra ID tenants.

If your account belongs to multiple tenants, ensure that the Tenant ID specified in `PurviewConfig` matches the Microsoft Purview instance that you intend to access.

Using an incorrect Tenant ID may result in:

- Authentication failures
- Authorization errors
- Accessing the wrong Microsoft Purview tenant

## Common Authentication and Configuration Errors

### Invalid Tenant ID

Verify that the Tenant ID is correct and that your account belongs to the specified Microsoft Entra ID tenant.

---

### Invalid Username

Verify that the username matches the Microsoft account (typically your corporate email address or assigned User Principal Name (UPN)) used to access Microsoft Purview.

---

### Incorrect API Endpoint

The SDK is designed to work with the **Microsoft Purview Unified Catalog API**. 

Using endpoints from the legacy **Azure Purview** APIs or other Microsoft Purview services may result in errors such as:

- `Unauthorized`
- `404 Not Found`
- `Resource not found`
- `Unsupported API`
- `Invalid request`

Ensure that the endpoint configured for your application corresponds to the Microsoft Purview Unified Catalog environment.

---

### Permission Denied

Authentication may succeed even if authorization fails.

Ensure that your Microsoft account has the required permissions to perform the requested operation in Microsoft Purview Unified Catalog.
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

## Relationship Support and Validation

The table below summarizes the relationship types currently reviewed during SDK development, including whether the relationship is documented by Microsoft and whether it has been validated through SDK testing.

| Source Resource | Target Resource | Documentation Support | Validation Status |
|-----------------|-----------------|:---------------------:|:-----------------:|
| **Data Product** | Glossary Term | ✅ | ✅ |
| | Data Asset | ✅ | ✅ |
| | Objective | ✅ | ✅ |
| | File | ✅ | ✅ |
| | Critical Data Element (CDE) | ❌ | ❌ (Not directly supported) |
| | Data Column | ❌ | ❌ |
| **Glossary Term** | Data Asset | ✅ | ✅ |
| | Data Column | ✅ | ✅ |
| | Critical Data Element (CDE) | ✅ | ✅ |
| **Critical Data Element (CDE)** | Glossary Term | ✅ | ✅ |
| | Data Column | ✅ | ✅ |
| | Data Product | ❌ | ❌ (Not directly supported) |
| **Data Asset** | Data Product | ✅ | ✅ |
| | Glossary Term | ✅ | ✅ |
| | Data Column | ✅ | ✅ |
| **Data Column** | Data Asset | ✅ | ✅ |
| | Glossary Term | ✅ | ✅ |
| | Critical Data Element (CDE) | ✅ | ✅ |

### Validation Status

- ✅ **Validated** – The relationship has been successfully tested using the SDK.
- ⏳ **Pending Validation** – The relationship is documented or expected to be supported but has not yet been fully validated.
- ❌ **Not Supported** – Microsoft Purview does not provide a supported direct relationship for this resource pair.
- ❌ **Not Directly Supported** – No direct relationship API exists, but the relationship can be established indirectly through another supported resource.

### Notes

#### Data Product ↔ Critical Data Element (CDE)

Microsoft Purview does not currently expose a direct relationship between **Data Products** and **Critical Data Elements (CDEs)**.

However, the relationship can be established indirectly through the Data Map:

1. Associate the **Critical Data Element** with a **Data Asset** or **Data Column**.
2. Associate the same **Data Asset** with a **Data Product**.
3. Microsoft Purview automatically displays the related CDE under the corresponding Data Product in the Unified Catalog.

The visual relationship is inferred by Microsoft Purview based on the shared Data Asset or Data Column rather than being created through a direct relationship API.

```text
Critical Data Element
        │
        ▼
Data Asset / Data Column
        │
        ▼
Data Product
```

Therefore, although **Data Product ↔ CDE** is marked as **Not Directly Supported**, the relationship can still appear in the Unified Catalog through the intermediate Data Asset or Data Column.

#### Data Column → Critical Data Element (CDE)

---

## Data Quality

Data Quality APIs supported by the SDK.

---

# Examples

The SDK includes a comprehensive set of example scripts demonstrating common Microsoft Purview Unified Catalog operations.

The examples are organized by resource type.

### Business Domains

- Create a Business Domain
- Update a Business Domain
- Delete a Business Domain
- List Business Domains

### Data Products

Examples include:

- Create a Data Product
- Update a Data Product
- Delete a Data Product
- List Data Products
- Navigate a Data Product
- List Data Product Relationships

### Glossary Terms

- Create a Glossary Term
- Update a Glossary Term
- Delete a Glossary Term
- List Glossary Terms

### Critical Data Elements (CDEs)

- Create a CDE
- Update a CDE
- Delete a CDE
- List CDEs

### Objectives and Key Results (OKRs)

- Create an Objective
- Update an Objective
- Delete an Objective

### Relationships

Relationship examples include:

- Data Product → Business Domain
- Data Product → Data Asset
- Data Product → Glossary Term
- Data Product → Objective
- Glossary Term → Data Asset
- Glossary Term → Data Column
- Glossary Term → Critical Data Element (CDE)
- Critical Data Element → Data Column
- Data Asset → Data Product
- Data Column → Data Asset

### Properties

Examples for retrieving Microsoft Purview resources include:

- Get Data Asset
- List Business Domains
- List Data Products
- List Glossary Terms
- List Critical Data Elements (CDEs)
- List Policies
- List Data Product Relationships

### Policies

- List Policies

More examples will be added as additional SDK features become available.
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
