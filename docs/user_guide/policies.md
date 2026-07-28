# Policies

Microsoft Purview Policies define governance rules, standards, and controls that apply to Microsoft Purview resources.

The current version of the Purview Unified SDK provides **read-only** access to Policies.

The SDK currently supports:

- List Policies
- Inspect Policy properties

---

## Before You Begin

The examples in this guide assume that authentication and client configuration have already been completed.

A configured client should be available as:

```python
client
```

For complete setup instructions, see:

- [Authentication](../getting_started/authentication.md)
- [Configuration](../getting_started/configuration.md)

---

## List Policies

Use `client.policies.list_all()` to retrieve all Microsoft Purview Policies available in the current environment.

```python
policies = client.policies.list_all()
```

The method returns a Python list containing Policy model objects.

---

## List Example

```python
def list_policies(client) -> None:
    """
    List Microsoft Purview Policies.
    """
    policies = client.policies.list_all()

    print(
        f"Found {len(policies)} policies."
    )

    for index, policy in enumerate(
        policies,
        start=1,
    ):
        print("=" * 80)
        print(
            f"Policy {index}"
        )
        print("=" * 80)
        print("ID:", policy.id)
        print("Name:", policy.name)
        print(
            "Version:",
            policy.version,
        )
        print(
            "Description:",
            policy.description,
        )
        print(
            "Entity Type:",
            policy.entity_type,
        )
        print(
            "Entity Reference:",
            policy.entity_reference_name,
        )
```

Call the function using:

```python
list_policies(client)
```

The complete runnable example is available in:

```text
examples/policies/list_policies.py
```

The example retrieves all Policies and prints their primary properties. :contentReference[oaicite:0]{index=0}

---

## Policy Model

Each Policy is returned as a Policy model object.

Common properties include:

| Property | Description |
|----------|-------------|
| `id` | Unique identifier of the Policy. |
| `name` | Policy name. |
| `version` | Policy version. |
| `description` | Policy description. |
| `entity_type` | Type of resource associated with the Policy. |
| `entity_reference_name` | Name of the referenced Microsoft Purview resource. |

Example:

```python
print(policy.id)
print(policy.name)
print(policy.version)
print(policy.description)
print(policy.entity_type)
print(policy.entity_reference_name)
```

---

## Accessing Individual Policies

Because `policies` is a list, you can iterate through all returned Policy objects.

```python
for policy in policies:
    print(policy.name)
    print(policy.version)
    print()
```

You can also access an individual item by index.

```python
first_policy = policies[0]

print(first_policy.id)
print(first_policy.name)
```

!!! warning "Check the List Before Accessing an Item"

    Do not access `policies[0]` before confirming that the list contains at least one item.

    If no Policies are returned, Python will raise:

    ```text
    IndexError: list index out of range
    ```

---

## Read-Only Resource

The current version of the SDK supports retrieving Policy information only.

Creating, updating, or deleting Policies is **not currently supported**.

Future SDK releases may add additional Policy management capabilities.

---

## Example File

| File | Purpose |
|------|---------|
| `examples/policies/list_policies.py` | Lists Microsoft Purview Policies and displays their properties. |

---

## Common Issues

### No Policies Returned

The list operation may return an empty list.

This may indicate that:

- No Policies exist in the current Microsoft Purview environment.
- The authenticated identity does not have permission to view Policies.

---

### Unauthorized or Forbidden

If the request returns `401 Unauthorized` or `403 Forbidden`, first verify that the SDK is using the Microsoft Purview **Unified Catalog** endpoint.

Then verify that the authenticated user or service principal has permission to access Policy resources.

---

## Next Steps

Continue with the **Data Map** guide to learn how Microsoft Purview resources are connected.

**Next:** [Data Map→](datamap.md)