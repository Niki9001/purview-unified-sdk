# Installation

This guide explains how to install the Purview Unified SDK and verify that it is working correctly.

---

## Prerequisites

Before installing the SDK, ensure that you have:

- Python 3.10 or later
- pip (Python package manager)

You can verify your Python installation by running:

```bash
python --version
```

---

## Install the SDK

Install the latest release from the Python Package Index (PyPI):

```bash
pip install purview-unified-sdk
```

---
## Verify the Installation

After installation, verify that the SDK can be imported successfully.

Start a Python interpreter:

```bash
python
```

Then run:

```python
from purview import PurviewClient, PurviewConfig

print(PurviewClient)
print(PurviewConfig)
```

If the installation was successful, you should see output similar to:

```text
<class 'purview.client.PurviewClient'>
<class 'purview.config.PurviewConfig'>
```

This confirms that the SDK has been installed correctly and is ready to use.

> **Note**
>
> The PyPI distribution name is `purview-unified-sdk`, while the Python import namespace is `purview`.
---

## Using a Virtual Environment

Using a virtual environment is recommended, especially when developing Python applications or working in enterprise environments.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**

```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Then install the SDK:

```bash
pip install purview-unified-sdk
```

---

## Troubleshooting

### `pip` is not recognized

If you receive an error similar to:

```text
'pip' is not recognized as an internal or external command
```

Ensure that Python and pip are installed correctly.

You can also install the SDK using:

```bash
python -m pip install purview-unified-sdk
```

---

### Unsupported Python Version

If you receive an error similar to:

```text
ERROR: Package 'purview-unified-sdk' requires a different Python version
```

Verify that you are using Python 3.10 or later.

Check your Python version:

```bash
python --version
```

---

### Package Not Found

If pip cannot locate the package:

```text
ERROR: No matching distribution found for purview-unified-sdk
```

Upgrade pip and try again:

```bash
python -m pip install --upgrade pip
python -m pip install purview-unified-sdk
```

---

### Import Errors

If installation succeeds but importing the SDK fails, verify that you are using the correct import statement.

Correct:

```python
from purview import PurviewClient, PurviewConfig
```

> **Note**
>
> Install the SDK using:
>
> ```bash
> pip install purview-unified-sdk
> ```
>
> but import it using the `purview` namespace.

---

### Network or SSL Errors

In some corporate environments, package installation may fail because of network restrictions, proxy servers, firewalls, or SSL inspection.

You may encounter errors similar to:

```text
Connection timed out
SSL certificate verify failed
Failed to establish a new connection
```

If this occurs:

- Verify that your internet connection is available.
- If you are connected to a corporate network, consult your IT administrator regarding proxy or firewall settings.
- If possible, try installing the package from a different network to determine whether the issue is environment-specific.

> **Note**
>
> These errors are related to the network environment rather than the SDK itself.

---

## Next Steps

Once the SDK has been installed successfully, continue with the Authentication guide to configure Microsoft Entra ID authentication.

➡️ **Next:** [Authentication](authentication.md)