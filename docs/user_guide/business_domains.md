# Business Domains

Business Domains provide a top-level organizational structure for governance resources in Microsoft Purview Unified Catalog.

A Business Domain can represent a business function, department, subject area, or other organizational grouping. Data Products and related governance resources can then be organized under the appropriate Business Domain.

The Purview Unified SDK supports the following Business Domain operations:

- Create a Business Domain
- List Business Domains
- Inspect Business Domain properties
- Update a Business Domain
- Delete a Business Domain

---

## Before You Begin

The examples in this guide assume that authentication and client configuration have already been completed.

A configured client should be available as:

```python
client
```

For complete authentication and configuration examples, see:

- [Authentication](../getting_started/authentication.md)
- [Configuration](../getting_started/configuration.md)

---

## Create a Business Domain

Use `client.business_domains.create()` to create a new Business Domain.

### Configuration Values

The example uses environment variables for the domain properties. If an environment variable is not defined, the example uses the provided default value.

```python
import os


DOMAIN_NAME = os.getenv(
    "PURVIEW_NEW_DOMAIN_NAME",
    "SDK Test Business Domain",
)

DOMAIN_TYPE = os.getenv(
    "PURVIEW_NEW_DOMAIN_TYPE",
    "DataDomain",
)

DOMAIN_DESCRIPTION = os.getenv(
    "PURVIEW_NEW_DOMAIN_DESCRIPTION",
    (
        "Business domain created by the "
        "Purview Unified SDK example."
    ),
)
```

You may optionally add the following values to your `.env` file:

```text
PURVIEW_NEW_DOMAIN_NAME=SDK Test Business Domain
PURVIEW_NEW_DOMAIN_TYPE=DataDomain
PURVIEW_NEW_DOMAIN_DESCRIPTION=Business domain created by the Purview Unified SDK example.
```

### Create Example

### Top-Level and Child Business Domains

If no parent Business Domain is specified when creating a domain, Microsoft Purview creates it as a **top-level Business Domain**.

```python
domain = client.business_domains.create(
    name=DOMAIN_NAME,
    domain_type=DOMAIN_TYPE,
    description=DOMAIN_DESCRIPTION,
)
```

To create a child Business Domain, provide the ID of an existing Business Domain as the parent, provided that the SDK's `create()` method supports the corresponding parent parameter.

```python
domain = client.business_domains.create(
    name=DOMAIN_NAME,
    domain_type=DOMAIN_TYPE,
    description=DOMAIN_DESCRIPTION,
    parent_id=PARENT_DOMAIN_ID,
)
```

!!! note

    Omitting the parent ID creates a top-level Business Domain.

    When creating a child Business Domain, verify that the supplied parent ID belongs to an existing Business Domain in the same Microsoft Purview environment.
---

## List Business Domains

Use `client.business_domains.list()` to retrieve the Business Domains available in the current Microsoft Purview environment.

```python
domains = client.business_domains.list()
```

The method returns a Python list containing Business Domain model objects.

### List Example

```python
def list_business_domains(client) -> None:
    """
    List Microsoft Purview Business Domains and inspect
    the first returned object.
    """
    domains = client.business_domains.list()

    print("Collection type:")
    print(type(domains))

    print()
    print("Business Domain count:")
    print(len(domains))

    if not domains:
        print()
        print("No Business Domains were returned.")
        return

    first_domain = domains[0]

    print()
    print("First item type:")
    print(type(first_domain))

    print()
    print("First Business Domain properties:")
    print("ID:", first_domain.id)
    print("Name:", first_domain.name)
    print(
        "Description:",
        first_domain.description,
    )

    print()
    print("First Business Domain as a dictionary:")
    print(first_domain.to_dict())
```

Call the function using:

```python
list_business_domains(client)
```

Typical type information will look similar to:

```text
<class 'list'>
<class 'purview.models.business_domain.BusinessDomain'>
```

The exact model path may vary if the internal package structure changes.

### Accessing Individual Domains

Because `domains` is a list, you can iterate over all returned Business Domains:

```python
for domain in domains:
    print(domain.id)
    print(domain.name)
    print(domain.description)
    print()
```

You can also access a specific item by index:

```python
first_domain = domains[0]

print(first_domain.id)
print(first_domain.name)
print(first_domain.description)
```

!!! warning "Check the List Before Accessing an Item"

    Do not access `domains[0]` before confirming that the list contains at least one item.

    If no Business Domains are returned, accessing the first item will raise:

    ```text
    IndexError: list index out of range
    ```

    Use the following check:

    ```python
    if not domains:
        print("No Business Domains were returned.")
        return
    ```

### Converting a Domain to a Dictionary

Business Domain model objects provide a `to_dict()` method:

```python
domain_dict = domains[0].to_dict()

print(domain_dict)
```

This is useful when:

- Inspecting the complete response
- Serializing results
- Exporting data
- Converting model objects for additional processing

A complete runnable example is available at:

```text
examples/get_properties/list_business_domains.py
```

The supplied example confirms that `list()` returns a list, inspects the first returned model object, reads its properties, and converts it to a dictionary. :contentReference[oaicite:1]{index=1}

---

## Update a Business Domain

Use `client.business_domains.update()` to update an existing Business Domain.

The operation requires the unique ID of the Business Domain.

### Update Values

```python
DOMAIN_ID = (
    "11111111-1111-1111-1111-111111111111"
)

NEW_DOMAIN_NAME = (
    "SDK Test Business Domain Updated"
)

NEW_DOMAIN_DESCRIPTION = (
    "Business domain updated by the "
    "Purview Unified SDK example."
)
```

!!! danger "Replace the Example Domain ID"

    The value shown for `DOMAIN_ID` is a masked example.

    Replace it with the ID of an existing Business Domain in your own Microsoft Purview environment.

    Using an invalid or nonexistent ID will cause the update operation to fail.

You may also store the ID in your `.env` file:

```text
PURVIEW_DOMAIN_ID=11111111-1111-1111-1111-111111111111
```

Then load it using:

```python
import os

DOMAIN_ID = os.environ["PURVIEW_DOMAIN_ID"]
```

### Update Example

```python
def update_business_domain(client) -> None:
    """
    Update an existing Microsoft Purview Business Domain.
    """
    print("=" * 80)
    print("Business Domain - Update")
    print("=" * 80)
    print("Domain ID:", DOMAIN_ID)
    print("New name:", NEW_DOMAIN_NAME)
    print(
        "New description:",
        NEW_DOMAIN_DESCRIPTION,
    )

    domain = client.business_domains.update(
        DOMAIN_ID,
        name=NEW_DOMAIN_NAME,
        description=NEW_DOMAIN_DESCRIPTION,
    )

    print()
    print("=" * 80)
    print("Business Domain updated successfully")
    print("=" * 80)
    print("ID:", domain.id)
    print("Name:", domain.name)
    print(
        "Description:",
        domain.description,
    )
    print("Status:", domain.status)

    print()
    print("Updated object:")
    print(domain)
```

Call the function using:

```python
update_business_domain(client)
```

The update operation returns the updated Business Domain object.

The example updates the domain name and description, then prints the returned ID, name, description, status, and full model object. :contentReference[oaicite:2]{index=2}

### Partial Updates

Only provide the properties that should be changed.

For example, to update only the description:

```python
domain = client.business_domains.update(
    DOMAIN_ID,
    description=(
        "Updated Business Domain description."
    ),
)
```

Do not intentionally replace existing values with empty strings unless that behavior has been verified for the relevant Microsoft Purview API version.

---

## Delete a Business Domain

Use `client.business_domains.delete()` to delete an existing Business Domain.

The operation requires the unique Business Domain ID.

### Delete Value

```python
DOMAIN_ID = (
    "11111111-1111-1111-1111-111111111111"
)
```

!!! danger "Replace the Example Domain ID"

    Replace the masked value with the ID of the Business Domain that you intend to delete.

    Carefully verify the ID before running the example.

### Delete Example

```python
def delete_business_domain(client) -> None:
    """
    Delete an existing Microsoft Purview Business Domain.
    """
    print("=" * 80)
    print("Business Domain - Delete")
    print("=" * 80)
    print("Domain ID:", DOMAIN_ID)

    confirmation = input(
        "Type DELETE to confirm deletion: "
    ).strip()

    if confirmation != "DELETE":
        print("Deletion cancelled.")
        return

    client.business_domains.delete(
        DOMAIN_ID
    )

    print()
    print("=" * 80)
    print("Business Domain deleted successfully")
    print("=" * 80)
    print("Deleted domain ID:", DOMAIN_ID)
```

Call the function using:

```python
delete_business_domain(client)
```

Before deleting the domain, the example requires the user to enter:

```text
DELETE
```

Any other input cancels the operation.

The runnable example includes this confirmation step to reduce the risk of accidental deletion. :contentReference[oaicite:3]{index=3}

!!! danger "Deletion Is Destructive"

    Deleting a Business Domain is a destructive operation.

    Before running the delete example:

    - Confirm that the Business Domain ID is correct.
    - Confirm that the domain is no longer required.
    - Review any resources associated with the domain.
    - Test the operation in a non-production environment whenever possible.

    The confirmation prompt protects the example script, but it does not provide transaction rollback or recovery.

---

## Business Domain Model

Create and update operations return a Business Domain model object. The list operation returns a list of these model objects.

Common properties demonstrated by the examples include:

| Property | Description |
|---|---|
| `id` | Unique identifier of the Business Domain. |
| `name` | Display name of the Business Domain. |
| `description` | Business description of the domain. |
| `status` | Current resource status. |
| `to_dict()` | Converts the model into a dictionary. |

Example:

```python
print(domain.id)
print(domain.name)
print(domain.description)
print(domain.status)
print(domain.to_dict())
```

Not every operation necessarily returns the same fields. Inspect the returned model or use `to_dict()` when you need to review the complete response.

---

## Complete Operation Pattern

A typical Business Domain workflow is:

```text
Create
  ↓
Record the returned ID
  ↓
List and inspect the domain
  ↓
Update the domain
  ↓
Delete it when it is no longer required
```

The ID returned during creation should be saved if the domain will later be updated, deleted, or associated with another resource.

For example:

```python
domain = client.business_domains.create(
    name="Finance",
    domain_type="DataDomain",
    description="Finance Business Domain.",
)

domain_id = domain.id

print("Created domain ID:", domain_id)
```

---

## Example Files

| File | Purpose |
|---|---|
| `examples/domains/create_domain.py` | Creates a Business Domain and prints the returned object. |
| `examples/get_properties/list_business_domains.py` | Lists domains and inspects the first returned model. |
| `examples/domains/update_domain.py` | Updates the name and description of an existing domain. |
| `examples/domains/delete_domain.py` | Deletes an existing domain after explicit confirmation. |

---

## Common Issues

### No Business Domains Returned

The list operation may return an empty list:

```python
domains = client.business_domains.list()

if not domains:
    print("No Business Domains were returned.")
```

This does not necessarily indicate an SDK error. The authenticated account may not have access to any domains, or no domains may exist in the current environment.

### Domain Not Found

Update or delete operations can fail when the supplied ID:

- Does not exist
- Belongs to another environment
- Has already been deleted
- Was copied incorrectly

Verify the resource ID in Microsoft Purview before retrying the operation.

### Unauthorized or Forbidden

If the request returns `401 Unauthorized` or `403 Forbidden`, first verify that the SDK is using the Microsoft Purview **Unified Catalog** endpoint rather than a classic Purview Data Catalog endpoint.

Also verify that the authenticated user, service principal, or managed identity has permission to perform the requested operation.

### Delete Operation Fails

A Business Domain may not be deletable while related resources still depend on it.

Review its Data Products and other associated resources before retrying deletion.

---

## Next Steps

After creating a Business Domain, continue with the Data Products guide.

**Next:** [Data Products →](data_products.md)