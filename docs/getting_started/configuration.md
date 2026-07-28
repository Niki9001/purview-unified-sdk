# Configuration

This guide explains how to configure the Purview Unified SDK before running the example applications.

The SDK itself does not require any specific configuration mechanism. However, the example programs included with the SDK use environment variables loaded from a `.env` file.

---

## Using a `.env` File

The example applications use the `python-dotenv` package to load configuration values from a `.env` file.

Create a file named `.env` in the project root.

Example:

```text
PURVIEW_TENANT_ID=<your-tenant-id>

PURVIEW_USERNAME=<your-email>

PURVIEW_CLIENT_ID=<your-client-id>

PURVIEW_CLIENT_SECRET=<your-client-secret>
```

Only the variables required by the selected authentication method need to be provided.

---

## Loading the Configuration

The example applications load the configuration using:

```python
from dotenv import load_dotenv

load_dotenv()
```

Configuration values can then be accessed using:

```python
import os

tenant_id = os.environ["PURVIEW_TENANT_ID"]
```

---

## Authentication-Specific Configuration

Different authentication methods require different environment variables.

### Interactive Browser Authentication

```text
PURVIEW_TENANT_ID
PURVIEW_USERNAME
```

---

### Device Code Authentication

```text
PURVIEW_TENANT_ID
```

---

### Client Secret Authentication

```text
PURVIEW_TENANT_ID
PURVIEW_CLIENT_ID
PURVIEW_CLIENT_SECRET
```

---

### Managed Identity Authentication

```text
PURVIEW_TENANT_ID
```

---

### Default Azure Credential

```text
PURVIEW_TENANT_ID
```

---

## Security Recommendations

Never commit your `.env` file to source control.

Add the following entry to your `.gitignore` file:

```text
.env
```

Store secrets such as client secrets only in secure locations.

---
Example:

```text
# Microsoft Entra ID
PURVIEW_TENANT_ID=12345678-1234-1234-1234-123456789abc
PURVIEW_USERNAME=john.smith@contoso.com

# Common resource IDs used by the example applications
PURVIEW_DOMAIN_ID=11111111-1111-1111-1111-111111111111
PURVIEW_DATA_PRODUCT_ID=22222222-2222-2222-2222-222222222222
PURVIEW_DATA_ASSET_ID=33333333-3333-3333-3333-333333333333
PURVIEW_GLOSSARY_TERM_ID=44444444-4444-4444-4444-444444444444
PURVIEW_DATA_PRODUCT_OWNER_ID=55555555-5555-5555-5555-555555555555

# Service Principal 
PURVIEW_CLIENT_ID=66666666-6666-6666-6666-666666666666
PURVIEW_CLIENT_SECRET=<your-client-secret>
```

Only the variables required by the selected authentication method need to be provided.
---

## Next Steps

After configuring the required environment variables, continue with the **Quick Start** guide.

➡️ **Next:** [Quick Start](quickstart.md)