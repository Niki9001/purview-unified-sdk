# Data Products

Data Products represent business-owned collections of data in Microsoft Purview Unified Catalog.

A Data Product belongs to a Business Domain and can include descriptive metadata, ownership information, update frequency, business use, linked Data Assets, Glossary Terms, Objectives, and other governance resources.

The Purview Unified SDK supports the following Data Product operations:

- Create a Data Product
- List Data Products
- Inspect Data Product properties
- Update a Data Product
- Delete a Data Product

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

A Data Product must be created within an existing Business Domain. You therefore need the ID of the target Business Domain before running the create example.

---

## Create a Data Product

Use `client.data_products.create()` to create a new Data Product.

### Required Resource IDs

The example requires:

- A Business Domain ID
- A Data Product owner ID

```python
DOMAIN_ID = (
    "11111111-1111-1111-1111-111111111111"
)

OWNER_ID = os.environ[
    "PURVIEW_DATA_PRODUCT_OWNER_ID"
]
```

!!! danger "Replace the Example IDs"

    The IDs shown in this guide are masked examples.

    Replace `DOMAIN_ID` with the ID of an existing Business Domain in your Microsoft Purview environment.

    Replace `PURVIEW_DATA_PRODUCT_OWNER_ID` with the correct owner identity ID.

    Using an invalid Domain ID or owner ID will cause the create operation to fail.

You may store both values in your `.env` file:

```text
PURVIEW_DOMAIN_ID=11111111-1111-1111-1111-111111111111
PURVIEW_DATA_PRODUCT_OWNER_ID=22222222-2222-2222-2222-222222222222
```

Then load them using:

```python
DOMAIN_ID = os.environ[
    "PURVIEW_DOMAIN_ID"
]

OWNER_ID = os.environ[
    "PURVIEW_DATA_PRODUCT_OWNER_ID"
]
```

---

### Data Product Values

```python
DATA_PRODUCT_NAME = (
    "SDK Test Data Product"
)

DATA_PRODUCT_DESCRIPTION = (
    "Data product created by the "
    "Purview Unified SDK example."
)

DATA_PRODUCT_BUSINESS_USE = (
    "Used to test Data Product create, "
    "update, and delete operations."
)
```

The example creates a Data Product with:

- Type: `Master`
- Status: `DRAFT`
- Update frequency: `Daily`
- One owner contact

---

### Owner Contact

The owner is provided through the `contacts` object:

```python
contacts = {
    "owner": [
        {
            "id": OWNER_ID,
            "description": (
                "Owner of the SDK test "
                "Data Product."
            ),
        }
    ]
}
```

The `owner` value contains a list because a Data Product may support one or more contacts depending on the Microsoft Purview configuration and API behavior.

---

### Create Example

```python
def create_data_product(client) -> None:
    """
    Create a Microsoft Purview Data Product.
    """
    contacts = {
        "owner": [
            {
                "id": OWNER_ID,
                "description": (
                    "Owner of the SDK test "
                    "Data Product."
                ),
            }
        ]
    }

    print("=" * 80)
    print("Data Product - Create")
    print("=" * 80)
    print("Domain ID:", DOMAIN_ID)
    print("Name:", DATA_PRODUCT_NAME)
    print("Type: Master")
    print("Status: DRAFT")
    print("Owner ID:", OWNER_ID)
    print(
        "Description:",
        DATA_PRODUCT_DESCRIPTION,
    )

    data_product = (
        client.data_products.create(
            name=DATA_PRODUCT_NAME,
            domain_id=DOMAIN_ID,
            contacts=contacts,
            data_product_type="Master",
            status="DRAFT",
            description=(
                DATA_PRODUCT_DESCRIPTION
            ),
            business_use=(
                DATA_PRODUCT_BUSINESS_USE
            ),
            update_frequency="Daily",
        )
    )

    print()
    print("=" * 80)
    print(
        "Data Product created successfully"
    )
    print("=" * 80)
    print("ID:", data_product.id)
    print("Name:", data_product.name)
    print(
        "Domain ID:",
        data_product.domain_id,
    )
    print("Type:", data_product.type)
    print("Status:", data_product.status)
    print(
        "Description:",
        data_product.description,
    )
    print(
        "Business use:",
        data_product.business_use,
    )
    print(
        "Update frequency:",
        data_product.update_frequency,
    )
    print(
        "Contacts:",
        data_product.contacts,
    )

    print()
    print("Created object:")
    print(data_product)
```

Call the function after creating the authenticated client:

```python
create_data_product(client)
```

The complete runnable example is available at:

```text
examples/data_products/create_data_product.py
```

The example creates a Data Product within an existing Business Domain, assigns an owner, and prints the returned object and its main properties. :contentReference[oaicite:0]{index=0}

---

### Returned Data Product

The create operation returns a Data Product model object.

Common returned properties demonstrated by the example include:

```python
data_product.id
data_product.name
data_product.domain_id
data_product.type
data_product.status
data_product.description
data_product.business_use
data_product.update_frequency
data_product.contacts
```

Because `domain_id` is supplied during creation, the new Data Product is created within that Business Domain.

Save the returned Data Product ID if the resource will later be updated, deleted, or linked to other resources:

```python
data_product_id = data_product.id

print(
    "Created Data Product ID:",
    data_product_id,
)
```

---

## List Data Products

Use `client.data_products.list()` to retrieve Data Products available in the current Microsoft Purview environment.

```python
data_products = client.data_products.list()
```

The method returns a Python list containing Data Product model objects.

---

### List Example

```python
def list_data_products(client) -> None:
    """
    List Microsoft Purview Data Products and inspect
    the first returned object.
    """
    data_products = client.data_products.list()

    print(type(data_products))
    print(
        "Data Product count:",
        len(data_products),
    )

    if not data_products:
        print("No Data Products were returned.")
        return

    first = data_products[0]

    print(type(first))
    print()
    print(first.id)
    print(first.name)
    print(first.status)
    print(first.type)
    print(first.domain_id)
    print(first.asset_count)

    print()
    print(first.to_dict())
```

Call the function using:

```python
list_data_products(client)
```

The complete runnable example is available at:

```text
examples/get_properties/list_data_products.py
```

The supplied example verifies that the result is a list, prints the number of returned Data Products, inspects the first model object, and converts it to a dictionary. :contentReference[oaicite:1]{index=1}

---

### Accessing Individual Data Products

Because `data_products` is a list, you can iterate over all returned resources:

```python
for data_product in data_products:
    print("ID:", data_product.id)
    print("Name:", data_product.name)
    print("Status:", data_product.status)
    print("Type:", data_product.type)
    print("Domain ID:", data_product.domain_id)
    print("Asset count:", data_product.asset_count)
    print()
```

You can also access an individual item by index:

```python
first = data_products[0]

print(first.id)
print(first.name)
print(first.status)
```

!!! warning "Check the List Before Accessing an Item"

    Do not access `data_products[0]` before confirming that the list is not empty.

    If no Data Products are returned, accessing the first item will raise:

    ```text
    IndexError: list index out of range
    ```

    Use:

    ```python
    if not data_products:
        print("No Data Products were returned.")
        return
    ```

---

### Converting a Data Product to a Dictionary

Data Product model objects provide a `to_dict()` method:

```python
data_product_dict = (
    data_products[0].to_dict()
)

print(data_product_dict)
```

This is useful when:

- Inspecting the complete response
- Exporting Data Products
- Serializing model data
- Comparing fields across resources
- Preparing data for additional processing

---

## Update a Data Product

Use `client.data_products.update()` to update an existing Data Product.

The operation requires the unique Data Product ID.

---

### Update Values

```python
DATA_PRODUCT_ID = (
    "33333333-3333-3333-3333-333333333333"
)

NEW_DATA_PRODUCT_NAME = (
    "SDK Test Data Product Updated"
)

NEW_DESCRIPTION = (
    "Data product updated by the "
    "Purview Unified SDK example."
)

NEW_BUSINESS_USE = (
    "Used to verify the Data Product "
    "update operation."
)

NEW_UPDATE_FREQUENCY = "Weekly"
```

!!! danger "Replace the Example Data Product ID"

    The value shown for `DATA_PRODUCT_ID` is a masked example.

    Replace it with the ID of an existing Data Product in your own Microsoft Purview environment.

    Using a nonexistent or incorrect ID will cause the update operation to fail.

You may store the ID in `.env`:

```text
PURVIEW_DATA_PRODUCT_ID=33333333-3333-3333-3333-333333333333
```

Then load it using:

```python
DATA_PRODUCT_ID = os.environ[
    "PURVIEW_DATA_PRODUCT_ID"
]
```

---

### Update Example

```python
def update_data_product(client) -> None:
    """
    Update an existing Microsoft Purview Data Product.
    """
    print("=" * 80)
    print("Data Product - Update")
    print("=" * 80)
    print(
        "Data Product ID:",
        DATA_PRODUCT_ID,
    )
    print(
        "New name:",
        NEW_DATA_PRODUCT_NAME,
    )
    print(
        "New description:",
        NEW_DESCRIPTION,
    )
    print(
        "New business use:",
        NEW_BUSINESS_USE,
    )
    print(
        "New update frequency:",
        NEW_UPDATE_FREQUENCY,
    )

    data_product = (
        client.data_products.update(
            DATA_PRODUCT_ID,
            name=NEW_DATA_PRODUCT_NAME,
            description=NEW_DESCRIPTION,
            business_use=NEW_BUSINESS_USE,
            update_frequency=(
                NEW_UPDATE_FREQUENCY
            ),
        )
    )

    print()
    print("=" * 80)
    print(
        "Data Product updated successfully"
    )
    print("=" * 80)
    print("ID:", data_product.id)
    print("Name:", data_product.name)
    print(
        "Domain ID:",
        data_product.domain_id,
    )
    print("Type:", data_product.type)
    print("Status:", data_product.status)
    print(
        "Description:",
        data_product.description,
    )
    print(
        "Business use:",
        data_product.business_use,
    )
    print(
        "Update frequency:",
        data_product.update_frequency,
    )
    print(
        "Contacts:",
        data_product.contacts,
    )

    print()
    print("Updated object:")
    print(data_product)
```

Call the function using:

```python
update_data_product(client)
```

The update example changes:

- Name
- Description
- Business use
- Update frequency

It then prints the updated model properties and the full returned object. :contentReference[oaicite:2]{index=2}

---

### Partial Updates

Only provide the fields that should be changed.

For example, to update only the description:

```python
data_product = (
    client.data_products.update(
        DATA_PRODUCT_ID,
        description=(
            "Updated Data Product description."
        ),
    )
)
```

To update only the frequency:

```python
data_product = (
    client.data_products.update(
        DATA_PRODUCT_ID,
        update_frequency="Monthly",
    )
)
```

Do not replace existing values with empty strings unless that behavior has been verified for the selected Microsoft Purview API version.

---

## Delete a Data Product

Use `client.data_products.delete()` to delete an existing Data Product.

The operation requires the unique Data Product ID.

---

### Delete Value

```python
DATA_PRODUCT_ID = (
    "33333333-3333-3333-3333-333333333333"
)
```

!!! danger "Replace the Example Data Product ID"

    Replace the masked value with the ID of the Data Product that you intend to delete.

    Carefully verify the ID before running the delete operation.

---

### Delete Example

```python
def delete_data_product(client) -> None:
    """
    Delete an existing Microsoft Purview Data Product.
    """
    print("=" * 80)
    print("Data Product - Delete")
    print("=" * 80)
    print(
        "Data Product ID:",
        DATA_PRODUCT_ID,
    )

    confirmation = input(
        "Type DELETE to confirm deletion: "
    ).strip()

    if confirmation != "DELETE":
        print("Deletion cancelled.")
        return

    client.data_products.delete(
        DATA_PRODUCT_ID,
    )

    print()
    print("=" * 80)
    print(
        "Data Product deleted successfully"
    )
    print("=" * 80)
    print(
        "Deleted Data Product ID:",
        DATA_PRODUCT_ID,
    )
```

Call the function using:

```python
delete_data_product(client)
```

Before deleting the resource, the example requires the user to enter:

```text
DELETE
```

Any other input cancels the operation.

The complete runnable example is available at:

```text
examples/data_products/delete_data_product.py
```

The confirmation step is included to reduce the risk of accidental deletion. :contentReference[oaicite:3]{index=3}

!!! danger "Deletion Is Destructive"

    Deleting a Data Product is a destructive operation.

    Before running the delete example:

    - Confirm that the Data Product ID is correct.
    - Confirm that the Data Product is no longer required.
    - Review linked Data Assets and other relationships.
    - Test the operation in a non-production environment whenever possible.

    The confirmation prompt does not provide rollback or recovery.

---

## Data Product Model

Create and update operations return a Data Product model object. The list operation returns a list of these objects.

Common properties demonstrated by the examples include:

| Property | Description |
|---|---|
| `id` | Unique identifier of the Data Product. |
| `name` | Display name. |
| `domain_id` | ID of the containing Business Domain. |
| `type` | Data Product type, such as `Master`. |
| `status` | Current status, such as `DRAFT`. |
| `description` | Description of the Data Product. |
| `business_use` | Intended business use. |
| `update_frequency` | Expected update frequency. |
| `contacts` | Owner and other contact information. |
| `asset_count` | Number of associated Data Assets, when returned. |
| `to_dict()` | Converts the model object into a dictionary. |

Example:

```python
print(data_product.id)
print(data_product.name)
print(data_product.domain_id)
print(data_product.type)
print(data_product.status)
print(data_product.description)
print(data_product.business_use)
print(data_product.update_frequency)
print(data_product.contacts)
print(data_product.to_dict())
```

Not every endpoint necessarily returns every property. Use `to_dict()` when you need to inspect the full response.

---

## Complete Operation Pattern

A typical Data Product workflow is:

```text
Create a Business Domain
        ↓
Create a Data Product in that Domain
        ↓
Record the returned Data Product ID
        ↓
List and inspect the Data Product
        ↓
Add relationships and Data Assets
        ↓
Update its metadata
        ↓
Delete it when it is no longer required
```

The returned ID is required for many later operations, including:

- Updating the Data Product
- Deleting the Data Product
- Adding Data Assets
- Adding Glossary Terms
- Adding Objectives
- Navigating related resources

---

## Example Files

| File | Purpose |
|---|---|
| `examples/data_products/create_data_product.py` | Creates a Data Product with owner and metadata. |
| `examples/get_properties/list_data_products.py` | Lists Data Products and inspects the first model object. |
| `examples/data_products/update_data_product.py` | Updates Data Product metadata. |
| `examples/data_products/delete_data_product.py` | Deletes a Data Product after explicit confirmation. |

---

## Common Issues

### Invalid Business Domain ID

A create operation can fail when the supplied `domain_id`:

- Does not exist
- Belongs to another environment
- Was copied incorrectly
- Is inaccessible to the authenticated identity

Verify the Business Domain ID before retrying.

### Invalid Owner ID

The owner ID must identify a valid user or supported identity in the current environment.

Using an email address where the API expects an identity ID may cause the request to fail.

### No Data Products Returned

The list operation may return an empty list:

```python
data_products = (
    client.data_products.list()
)

if not data_products:
    print("No Data Products were returned.")
```

This may mean that no Data Products exist or that the authenticated identity cannot access them.

### Data Product Not Found

Update and delete operations can fail when the supplied ID:

- Does not exist
- Has already been deleted
- Belongs to another tenant or environment
- Was entered incorrectly

### Unauthorized or Forbidden

If the request returns `401 Unauthorized` or `403 Forbidden`, first verify that the SDK is using the Microsoft Purview **Unified Catalog** endpoint rather than a classic Purview Data Catalog endpoint.

Then verify that the authenticated user, service principal, or managed identity has permission to manage Data Products.

### Delete Operation Fails

A Data Product may have linked Data Assets, Glossary Terms, Objectives, or other relationships.

Review those associations before retrying deletion.

---

## Next Steps

After creating and managing Data Products, continue with the Glossary Terms guide.

**Next:** [Glossary Terms →](glossary.md)