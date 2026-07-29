# Purview Unified SDK

**Purview Unified SDK** is a Python SDK for Microsoft Purview Unified Catalog.

It provides a simple and consistent Python interface for automating Microsoft Purview operations, including Business Domains, Data Products, Glossary Terms, Critical Data Elements (CDEs), Data Assets, Data Columns, Policies, Objectives and Key Results (OKRs), and resource relationships.

Whether you're building governance automation, migrating metadata, or integrating Microsoft Purview into your own applications, the SDK helps you work with the Unified Catalog through clean, reusable Python code.

## Why Purview Unified SDK?

Building automation with the Microsoft Purview REST APIs often requires handling authentication, pagination, request formatting, resource relationships, and other API-specific details before you can focus on your actual governance tasks.

Purview Unified SDK abstracts these complexities behind a clean, consistent, and Pythonic interface, allowing you to spend less time writing infrastructure code and more time automating Microsoft Purview.

### Key Features

- ✅ Unified programming model across multiple Microsoft Purview resource types
- ✅ Simple and intuitive Python APIs for common governance operations
- ✅ Built-in authentication support
- ✅ Automatic pagination for list operations
- ✅ Consistent relationship management across supported resources
- ✅ Strongly typed resource models
- ✅ Comprehensive documentation and runnable examples
- ✅ Designed for governance automation, reporting, and system migration workflows

### Currently Supported

- Business Domains
- Data Products
- Glossary Terms
- Critical Data Elements (CDEs)
- Data Assets
- Data Columns
- Objectives and Key Results (OKRs)
- Policies
- Resource Relationships
- Data Map

Unlike scripts that target a single endpoint, Purview Unified SDK provides a unified programming model across multiple Microsoft Purview resource types, making it easier to build automation workflows that span the entire Unified Catalog.

[Get started](getting_started/index.md){ .md-button .md-button--primary }
[View the user guide](user_guide/business_domains.md){ .md-button }
[Browse the API reference](api_reference/purview_client.md){ .md-button }

---

## Installation

Install the latest release from the Python Package Index:

```bash
pip install purview-unified-sdk
```

Import the SDK in Python:

```python
from purview import PurviewClient, PurviewConfig
```

---

## Quick Start

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

for domain in domains:
    print(domain.name)
```

[Read the full quick-start guide](getting_started/quickstart.md)

---

## Explore the Documentation

<div class="grid cards" markdown>

-   :material-rocket-launch-outline:{ .lg .middle } **Getting Started**

    ---

    Install the SDK, configure authentication, and run your first Microsoft Purview request.

    [Get started](getting_started/installation.md)

-   :material-book-open-page-variant-outline:{ .lg .middle } **User Guide**

    ---

    Learn how to work with Business Domains, Data Products, Glossary Terms, CDEs, Data Assets, Data Columns, OKRs, Policies, and Relationships.

    [Open the user guide](user_guide/business_domains.md)

-   :material-link-variant:{ .lg .middle } **Relationships**

    ---

    Understand supported Microsoft Purview relationships, directionality, indirect associations, and validation status.

    [Explore relationships](user_guide/relationships.md)


-   :material-api:{ .lg .middle } **API Reference**

    ---

    Review SDK clients, methods, parameters, return types, and model objects.

    [Browse the API reference](api_reference/purview_client.md)

-   :material-github:{ .lg .middle } **Examples**

    ---

    Explore runnable Python examples included in the repository.

    [View examples on GitHub](https://github.com/Niki9001/purview-unified-sdk/tree/main/examples)

</div>

---

## Supported Resources

The SDK currently provides functionality for:

- Business Domains
- Data Products
- Glossary Terms
- Critical Data Elements
- Data Assets
- Data Columns
- Objectives and Key Results
- Policies
- Resource relationships
- Resource property retrieval

---

## Package and Import Names

The PyPI distribution name is:

```text
purview-unified-sdk
```

The Python import package is:

```python
import purview
```

Therefore, install the package using:

```bash
pip install purview-unified-sdk
```

Then import its public classes using:

```python
from purview import PurviewClient, PurviewConfig
```

---

## Documentation Status

This documentation is being expanded alongside the SDK.

Validated behavior, supported relationships, known limitations, and complete examples will be documented throughout the User Guide and API Reference.

---

## About

**Purview Unified SDK** is an open-source Python SDK for Microsoft Purview Unified Catalog, developed and maintained by **Niki Zheng**.

### Contact

If you have questions, suggestions, or would like to report an issue, feel free to get in touch.

- **GitHub:** <https://github.com/Niki9001/purview-unified-sdk>
- **Issues:** <https://github.com/Niki9001/purview-unified-sdk/issues>

Contributions, feature requests, and bug reports are always welcome.

---

## License

This project is released under the MIT License.