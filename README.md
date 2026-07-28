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

The SDK authenticates using your Microsoft account.

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
