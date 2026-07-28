# Purview Client

The `PurviewClient` class is the primary entry point of the Purview Unified SDK.

After authentication, all SDK functionality is accessed through resource-specific clients exposed by `PurviewClient`.

---

## Creating a Client

Create a `PurviewClient` using a `PurviewConfig` object.

```python
config = PurviewConfig(
    tenant_id=os.environ[
        "PURVIEW_TENANT_ID"
    ],
)

with PurviewClient(
    config,
    username=os.environ[
        "PURVIEW_USERNAME"
    ],
) as client:

    ...
```

For authentication options, see the [Authentication](../getting_started/authentication.md) guide.

---

## Resource Clients

`PurviewClient` exposes the following resource clients.

| Client | Description |
|---------|-------------|
| `business_domains` | Manage Business Domains. |
| `data_products` | Manage Data Products. |
| `glossary` | Manage Glossary Terms. |
| `cdes` | Manage Critical Data Elements. |
| `data_assets` | Retrieve Data Assets from the Data Map. |
| `relationships` | Create and query relationships between resources. |
| `okrs` | Manage Objectives. |
| `policies` | Retrieve Microsoft Purview Policies. |

Example:

```python
with PurviewClient(
    config,
    username=username,
) as client:

    domains = (
        client.business_domains.list()
    )

    products = (
        client.data_products.list()
    )

    glossary_terms = (
        client.glossary.list()
    )
```

---

## Client Lifetime

`PurviewClient` is designed to be used as a context manager.

```python
with PurviewClient(
    config,
    username=username,
) as client:

    ...
```

Using the context manager ensures that any underlying resources are released correctly when the block exits.

---

## Client Structure

The SDK is organized around Microsoft Purview resource types.

```text
PurviewClient
│
├── business_domains
├── data_products
├── glossary
├── cdes
├── data_assets
├── relationships
├── okrs
└── policies
```

Each resource client contains the operations for a specific Microsoft Purview resource.

For example:

```python
client.business_domains.create(...)
client.data_products.update(...)
client.glossary.list(...)
client.cdes.delete(...)
client.relationships.create(...)
client.okrs.create_objective(...)
client.policies.list_all(...)
```

---

## Relationship Between Clients

Each client is responsible for a single resource type.

```text
PurviewClient
        │
        ├────────► Business Domains
        ├────────► Data Products
        ├────────► Glossary
        ├────────► Critical Data Elements
        ├────────► Data Assets
        ├────────► Relationships
        ├────────► Objectives
        └────────► Policies
```

Resource clients can be used together.

For example:

```text
Create a Business Domain
        ↓
Create a Data Product
        ↓
Create a Glossary Term
        ↓
Retrieve a Data Asset
        ↓
Create Relationships
```

---

## Thread Safety

A `PurviewClient` instance is intended to be used within the scope in which it is created.

For concurrent operations, create a separate client instance for each independent execution context.

---

## Next Steps

Choose the resource you want to work with from the **User Guide**.

Examples include:

- [Business Domains](../user_guide/business_domains.md)
- [Data Products](../user_guide/data_products.md)
- [Glossary](../user_guide/glossary.md)
- [Critical Data Elements](../user_guide/cdes.md)
- [Data Map](../user_guide/data_map.md)
- [Relationships](../user_guide/relationships.md)
- [Objectives and Key Results](../user_guide/okrs.md)
- [Policies](../user_guide/policies.md)