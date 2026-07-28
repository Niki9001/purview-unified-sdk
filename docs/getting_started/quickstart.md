# Quick Start

This guide demonstrates how to connect to Microsoft Purview Unified Catalog and make your first API request using the Purview Unified SDK.

---

## Before You Begin

Before running the example, ensure that you have completed the following steps:

- Installed the SDK
- Configured authentication
- Created a `.env` file with the required configuration values

!!! danger "Replace the Example Values"

    **The values shown below are examples only.**

    **You must replace them with your own Microsoft Entra ID tenant ID and account information before running the examples.**

    Using the example values will cause authentication to fail.

    ```text
    PURVIEW_TENANT_ID=12345678-1234-1234-1234-123456789abc
    PURVIEW_USERNAME=john.smith@contoso.com
    ```

---

## Run Your First Example

The SDK includes a collection of runnable example programs.

To verify that everything is configured correctly, run the following example:

```bash
python examples/get_properties/list_business_domains.py
```

This example:

- Loads configuration from the `.env` file.
- Creates a `PurviewConfig` object.
- Authenticates with Microsoft Entra ID.
- Connects to Microsoft Purview Unified Catalog.
- Retrieves all Business Domains.

The example code is shown below:

```python
from dotenv import load_dotenv
import os

from purview import (
    PurviewClient,
    PurviewConfig,
)

load_dotenv()

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:
    domains = client.business_domains.list()

print(f"Found {len(domains)} Business Domains.")
```

---

## Expected Output

If everything is configured correctly, you should see output similar to:

```text
Found 8 Business Domains.

Business Domain 1
Business Domain 2
Business Domain 3
...
```

The exact number of Business Domains depends on your Microsoft Purview environment.

---

## Next Steps

The SDK includes additional example programs organized by feature.

| Directory | Description |
|-----------|-------------|
| `auth_example` | Authentication examples |
| `domains` | Create, update, and delete Business Domains |
| `data_products` | Data Product operations |
| `glossary_terms` | Glossary Term operations |
| `cdes` | Critical Data Element (CDE) operations |
| `add_relationships` | Relationship examples |
| `okrs` | Objective and Key Result (OKR) operations |
| `policies` | Policy operations |
| `get_properties` | Read-only examples |

For a complete explanation of each resource, continue with the **User Guide**.

➡️ **Next:** [User Guide Overview](../user_guide/user_guide_overview.md)