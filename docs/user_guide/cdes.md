# Critical Data Elements

Critical Data Elements, commonly abbreviated as **CDEs**, identify data that is especially important to an organization.

A CDE may represent information that is critical for regulatory reporting, financial operations, customer processes, risk management, analytics, or other business activities.

In Microsoft Purview Unified Catalog, CDEs can be associated with Glossary Terms, Data Assets, and Data Columns to show where critical business information is defined and used.

A typical relationship pattern is:

```text
Business Domain
        │
        ▼
Critical Data Element
        │
        ├──────────────► Glossary Term
        │
        └──────────────► Data Column
```

The Purview Unified SDK supports the following CDE operations:

- Create a Critical Data Element
- List Critical Data Elements
- Inspect CDE properties
- Update a Critical Data Element
- Delete a Critical Data Element

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

Every CDE created by the example belongs to an existing Business Domain. You therefore need the ID of the target Business Domain before running the create example.

---

## Create a Critical Data Element

Use `client.cdes.create()` to create a new Critical Data Element.

### Required Business Domain ID

The create example reads the Business Domain ID from the `.env` file:

```python
DOMAIN_ID = os.environ[
    "PURVIEW_DOMAIN_ID"
]
```

Add the value to `.env`:

```text
PURVIEW_DOMAIN_ID=11111111-1111-1111-1111-111111111111
```

!!! danger "Replace the Example Domain ID"

    The value shown above is a masked example.

    Replace it with the ID of an existing Business Domain in your own Microsoft Purview environment.

    Using an invalid or inaccessible Domain ID will cause the create operation to fail.

---

### CDE Values

```python
CDE_NAME = (
    "SDK Test Critical Data Element"
)

CDE_DESCRIPTION = (
    "Critical Data Element created by the "
    "Purview Unified SDK example."
)

CDE_DATA_TYPE = (
    "TEXT"
)

CDE_STATUS = (
    "DRAFT"
)
```

The example creates the CDE with:

- Data type: `TEXT`
- Status: `DRAFT`
- An existing Business Domain ID
- A name and description

---

### Create Example

```python
def create_cde(client) -> None:
    """
    Create a Microsoft Purview Critical Data Element.
    """
    print("=" * 80)
    print("Critical Data Element - Create")
    print("=" * 80)
    print("Name:", CDE_NAME)
    print("Domain ID:", DOMAIN_ID)
    print("Data type:", CDE_DATA_TYPE)
    print("Status:", CDE_STATUS)
    print()

    cde = client.cdes.create(
        name=CDE_NAME,
        domain_id=DOMAIN_ID,
        data_type=CDE_DATA_TYPE,
        description=CDE_DESCRIPTION,
        status=CDE_STATUS,
    )

    print("=" * 80)
    print("Created Critical Data Element")
    print("=" * 80)
    print("ID:", cde.id)
    print("Name:", cde.name)
    print("Description:", cde.description)
    print("Status:", cde.status)
    print("Data type:", cde.data_type)
    print("Domain ID:", cde.domain_id)
```

Call the function after creating the authenticated client:

```python
create_cde(client)
```

The complete runnable example is available at:

```text
examples/cdes/create_cde.py
```

The example creates a CDE in an existing Business Domain and prints the returned ID, name, description, status, data type, and Domain ID. :contentReference[oaicite:0]{index=0}

---

### Draft Status

The example creates the CDE with:

```python
status="DRAFT"
```

Using `DRAFT` is appropriate when the CDE definition is still under review.

Before publishing or approving a CDE, confirm that:

- Its business meaning is clear
- Its data type is correct
- Its Domain assignment is correct
- Its related Glossary Terms are appropriate
- Its associated Data Columns have been validated
- Its governance ownership has been reviewed

---

### Data Type

The example uses:

```python
data_type="TEXT"
```

The data type describes the type of business information represented by the CDE.

Use values supported by your Microsoft Purview Unified Catalog environment and API version.

Do not assume that arbitrary data type strings will be accepted.

---

### Returned CDE

The create operation returns a Critical Data Element model object.

Common returned properties include:

```python
cde.id
cde.name
cde.description
cde.status
cde.data_type
cde.domain_id
```

The `domain_id` identifies the Business Domain containing the CDE.

Save the returned CDE ID if the resource will later be updated, deleted, or associated with other resources:

```python
cde_id = cde.id

print(
    "Created CDE ID:",
    cde_id,
)
```

---

## List Critical Data Elements

Use `client.cdes.query_models()` to retrieve CDEs as model objects.

```python
cdes = client.cdes.query_models()
```

Unlike some other resource clients that use `list()`, the CDE example uses `query_models()`.

The method returns a Python list containing Critical Data Element model objects. :contentReference[oaicite:1]{index=1}

---

### List Example

```python
def list_cdes(client) -> None:
    """
    List Microsoft Purview Critical Data Elements
    and inspect the first returned object.
    """
    cdes = client.cdes.query_models()

    print(type(cdes))
    print(
        "CDE count:",
        len(cdes),
    )

    if not cdes:
        print("No CDEs were returned.")
        return

    first_cde = cdes[0]

    print(type(first_cde))
    print()
    print(first_cde.id)
    print(first_cde.name)
    print(first_cde.description)
    print(first_cde.status)
    print(first_cde.data_type)
    print(first_cde.domain_id)

    print()
    print(first_cde.to_dict())
```

Call the function using:

```python
list_cdes(client)
```

The complete runnable example is available at:

```text
examples/get_properties/list_cdes.py
```

The supplied example confirms that `query_models()` returns a list, prints the number of returned CDEs, inspects the first model object, and converts it to a dictionary. :contentReference[oaicite:2]{index=2}

---

### Accessing Individual CDEs

Because `cdes` is a list, you can iterate over all returned CDEs:

```python
for cde in cdes:
    print("ID:", cde.id)
    print("Name:", cde.name)
    print(
        "Description:",
        cde.description,
    )
    print("Status:", cde.status)
    print(
        "Data type:",
        cde.data_type,
    )
    print(
        "Domain ID:",
        cde.domain_id,
    )
    print()
```

You can also access an individual item by index:

```python
first_cde = cdes[0]

print(first_cde.id)
print(first_cde.name)
print(first_cde.status)
```

!!! warning "Check the List Before Accessing an Item"

    Do not access `cdes[0]` before confirming that the list contains at least one item.

    If no CDEs are returned, Python will raise:

    ```text
    IndexError: list index out of range
    ```

    Use:

    ```python
    if not cdes:
        print("No CDEs were returned.")
        return
    ```

---

### Converting a CDE to a Dictionary

Critical Data Element model objects provide a `to_dict()` method:

```python
cde_dict = cdes[0].to_dict()

print(cde_dict)
```

This is useful when:

- Inspecting the complete response
- Exporting CDE metadata
- Serializing model data
- Comparing CDE properties
- Preparing results for reporting or validation

---

## Update a Critical Data Element

Use `client.cdes.update()` to update an existing CDE.

The operation requires the unique CDE ID.

---

### Update Values

```python
CDE_ID = (
    "22222222-2222-2222-2222-222222222222"
)

NEW_CDE_NAME = (
    "SDK Test Critical Data Element Updated"
)

NEW_DESCRIPTION = (
    "Critical Data Element updated by the "
    "Purview Unified SDK example."
)

NEW_DATA_TYPE = (
    "TEXT"
)

NEW_STATUS = (
    "DRAFT"
)
```

!!! danger "Replace the Example CDE ID"

    The value shown for `CDE_ID` is a masked example.

    Replace it with the ID of an existing Critical Data Element in your own Microsoft Purview environment.

    Using an invalid or nonexistent ID will cause the update operation to fail.

You may store the ID in `.env`:

```text
PURVIEW_CDE_ID=22222222-2222-2222-2222-222222222222
```

Then load it using:

```python
CDE_ID = os.environ[
    "PURVIEW_CDE_ID"
]
```

---

### Update Example

```python
def update_cde(client) -> None:
    """
    Update an existing Microsoft Purview
    Critical Data Element.
    """
    print("=" * 80)
    print("Critical Data Element - Update")
    print("=" * 80)
    print("CDE ID:", CDE_ID)
    print("New name:", NEW_CDE_NAME)
    print("New description:", NEW_DESCRIPTION)
    print("New data type:", NEW_DATA_TYPE)
    print("New status:", NEW_STATUS)
    print()

    cde = client.cdes.update(
        cde_id=CDE_ID,
        name=NEW_CDE_NAME,
        description=NEW_DESCRIPTION,
        data_type=NEW_DATA_TYPE,
        status=NEW_STATUS,
    )

    print("=" * 80)
    print("Updated Critical Data Element")
    print("=" * 80)
    print("ID:", cde.id)
    print("Name:", cde.name)
    print("Description:", cde.description)
    print("Status:", cde.status)
    print("Data type:", cde.data_type)
    print("Domain ID:", cde.domain_id)
```

Call the function using:

```python
update_cde(client)
```

The complete runnable example is available at:

```text
examples/cdes/update_cde.py
```

The example updates the CDE name, description, data type, and status, then prints the returned properties. :contentReference[oaicite:3]{index=3}

---

### Partial Updates

Only provide the fields that should be changed.

For example, to update only the description:

```python
cde = client.cdes.update(
    cde_id=CDE_ID,
    description=(
        "Updated CDE description."
    ),
)
```

To update only the status:

```python
cde = client.cdes.update(
    cde_id=CDE_ID,
    status="DRAFT",
)
```

To update the name and data type:

```python
cde = client.cdes.update(
    cde_id=CDE_ID,
    name="Updated Critical Field",
    data_type="TEXT",
)
```

Do not replace existing values with empty strings unless that behavior has been verified for the selected Microsoft Purview API version.

---

## Delete a Critical Data Element

Use `client.cdes.delete()` to delete an existing CDE.

The operation requires the unique CDE ID.

---

### Delete Value

```python
CDE_ID = (
    "22222222-2222-2222-2222-222222222222"
)
```

!!! danger "Replace the Example CDE ID"

    Replace the masked value with the ID of the Critical Data Element that you intend to delete.

    Carefully verify the ID before running the operation.

---

### Delete Example

```python
def delete_cde(client) -> None:
    """
    Delete an existing Microsoft Purview
    Critical Data Element.
    """
    print("=" * 80)
    print("Critical Data Element - Delete")
    print("=" * 80)
    print("CDE ID:", CDE_ID)
    print()

    client.cdes.delete(
        CDE_ID
    )

    print("=" * 80)
    print("Critical Data Element Deleted")
    print("=" * 80)
    print(
        "Deleted CDE ID:",
        CDE_ID,
    )
```

Call the function using:

```python
delete_cde(client)
```

The complete runnable example is available at:

```text
examples/cdes/delete_cde.py
```

The example deletes the specified CDE and prints the deleted CDE ID after the request completes. :contentReference[oaicite:4]{index=4}

!!! danger "Deletion Is Destructive"

    Deleting a Critical Data Element is a destructive operation.

    Before deleting a CDE:

    - Confirm that the CDE ID is correct.
    - Review all existing Glossary Term relationships.
    - Review linked Data Columns.
    - Review linked Data Assets.
    - Check whether the CDE appears indirectly under a Data Product.
    - Test deletion in a non-production environment whenever possible.

    Removing a CDE may affect the governance context shown for related resources.

---

## Critical Data Element Model

Create and update operations return a Critical Data Element model object. The list operation returns a list of these objects.

Common properties demonstrated by the examples include:

| Property | Description |
|---|---|
| `id` | Unique identifier of the CDE. |
| `name` | Display name of the CDE. |
| `description` | Business description. |
| `status` | Current lifecycle or publication status. |
| `data_type` | Data type assigned to the CDE. |
| `domain_id` | ID of the containing Business Domain. |
| `to_dict()` | Converts the model object into a dictionary. |

Example:

```python
print(cde.id)
print(cde.name)
print(cde.description)
print(cde.status)
print(cde.data_type)
print(cde.domain_id)
print(cde.to_dict())
```

Not every endpoint necessarily returns every property. Use `to_dict()` when you need to inspect the complete response.

---

## CDE Relationships

Critical Data Elements can be connected to other governance and technical resources.

Common supported relationship scenarios include:

- CDE → Glossary Term
- CDE → Data Column
- Glossary Term → CDE

A direct Data Product-to-CDE operation has not been identified.

Instead, the CDE may appear automatically under a Data Product when:

1. The CDE is linked to a Data Asset or Data Column.
2. The same Data Asset is linked to the Data Product.
3. Microsoft Purview infers and displays the CDE association.

```text
Critical Data Element
        │
        ▼
Data Asset or Data Column
        │
        ▼
Data Product
```

This is an indirect relationship rather than a direct Data Product-to-CDE API operation.

For the complete tested support matrix, see:

[Relationship Matrix](../api_reference/relationship_matrix.md)

---

## Complete Operation Pattern

A typical CDE workflow is:

```text
Create a Business Domain
        ↓
Create a CDE in that Domain
        ↓
Record the returned CDE ID
        ↓
List and inspect the CDE
        ↓
Link it to Glossary Terms or Data Columns
        ↓
Validate the related Data Map resources
        ↓
Update the CDE definition or status
        ↓
Delete it when it is no longer required
```

The returned CDE ID is required for later operations, including:

- Updating the CDE
- Deleting the CDE
- Linking it to a Glossary Term
- Linking it to a Data Column
- Validating indirect Data Product visibility

---

## Example Files

| File | Purpose |
|---|---|
| `examples/cdes/create_cde.py` | Creates a CDE and prints its returned properties. |
| `examples/get_properties/list_cdes.py` | Lists CDEs and inspects the first returned model object. |
| `examples/cdes/update_cde.py` | Updates an existing CDE. |
| `examples/cdes/delete_cde.py` | Deletes an existing CDE. |

---

## Common Issues

### Invalid Business Domain ID

A create operation can fail when the supplied `domain_id`:

- Does not exist
- Belongs to another environment
- Was copied incorrectly
- Is inaccessible to the authenticated identity

Verify the Business Domain ID before retrying.

### No CDEs Returned

The query may return an empty list:

```python
cdes = client.cdes.query_models()

if not cdes:
    print("No CDEs were returned.")
```

This may mean that no CDEs exist or that the authenticated identity cannot access them.

### CDE Not Found

Update and delete operations can fail when the supplied ID:

- Does not exist
- Has already been deleted
- Belongs to another environment
- Was entered incorrectly

### Invalid Data Type

The selected `data_type` may not be accepted by the current Microsoft Purview API.

Confirm that the value is supported before retrying.

### Unauthorized or Forbidden

If the request returns `401 Unauthorized` or `403 Forbidden`, first verify that the SDK is using the Microsoft Purview **Unified Catalog** endpoint rather than a classic Purview Data Catalog endpoint.

Then verify that the authenticated user, service principal, or managed identity has permission to manage Critical Data Elements.

### Delete Operation Fails

A CDE may be connected to Glossary Terms, Data Columns, Data Assets, or indirectly displayed under Data Products.

Review those relationships before retrying deletion.

---

## Next Steps

After creating and managing Critical Data Elements, continue with the Data Map guide.

**Next:** [Objectives and Key Results (OKRs) →](okrs.md)