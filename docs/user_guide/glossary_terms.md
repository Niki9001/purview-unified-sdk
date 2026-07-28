# Glossary Terms

Glossary Terms define the shared business vocabulary used throughout Microsoft Purview Unified Catalog.

A Glossary Term can describe a business concept, data definition, process, measurement, or other organizational terminology. Glossary Terms help connect business meaning with technical metadata by linking governance concepts to Data Assets, Data Columns, Critical Data Elements, and other supported resources.

A typical relationship pattern is:

```text
Business Domain
        │
        ▼
Glossary Term
        │
        ├──────────────┐
        ▼              ▼
   Data Asset      Data Column
        ▲
        │
Critical Data Element
```

The Purview Unified SDK supports the following Glossary Term operations:

- Create a Glossary Term
- List Glossary Terms
- Inspect Glossary Term properties
- Update a Glossary Term
- Delete a Glossary Term

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

Every Glossary Term created by the example belongs to an existing Business Domain. You therefore need the ID of the target Business Domain before running the create example.

---

## Create a Glossary Term

Use `client.glossary_terms.create()` to create a new Glossary Term.

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

### Create Example

```python
from pprint import pprint
import os


DOMAIN_ID = os.environ[
    "PURVIEW_DOMAIN_ID"
]


def create_glossary_term(client) -> None:
    """
    Create a Microsoft Purview Glossary Term.
    """
    term = client.glossary_terms.create(
        name="SDK Test Glossary Term",
        description=(
            "Created by the Purview Unified SDK."
        ),
        domain_id=DOMAIN_ID,
        status="DRAFT",
    )

    print("=" * 80)
    print("Glossary Term Created")
    print("=" * 80)

    print("ID:", term.id)
    print("Name:", term.name)
    print(
        "Description:",
        term.description,
    )
    print("Status:", term.status)
    print(
        "Domain ID:",
        term.domain_id,
    )

    print()
    print("=" * 80)
    print("Raw Object")
    print("=" * 80)

    pprint(term.to_dict())
```

Call the function after creating the authenticated client:

```python
create_glossary_term(client)
```

The complete runnable example is available at:

```text
examples/glossary_terms/create_glossary_term.py
```

The example creates a Glossary Term in an existing Business Domain, sets its initial status to `DRAFT`, prints the returned properties, and converts the model object to a dictionary. :contentReference[oaicite:0]{index=0}

---

### Draft Status

The example creates the Glossary Term with:

```python
status="DRAFT"
```

Using `DRAFT` is appropriate when the term is still being reviewed or developed.

Before publishing governance content, confirm that the name, definition, ownership, and related metadata are complete and approved according to your organization's governance process.

---

### Returned Glossary Term

The create operation returns a Glossary Term model object.

Common returned properties include:

```python
term.id
term.name
term.description
term.status
term.domain_id
```

The `domain_id` identifies the Business Domain containing the Glossary Term.

Save the returned Glossary Term ID if the term will later be updated, deleted, or associated with other resources:

```python
glossary_term_id = term.id

print(
    "Created Glossary Term ID:",
    glossary_term_id,
)
```

---

## List Glossary Terms

Use `client.glossary_terms.list()` to retrieve the Glossary Terms available in the current Microsoft Purview environment.

```python
terms = client.glossary_terms.list()
```

The method returns a Python list containing Glossary Term model objects.

---

### List Example

```python
def list_glossary_terms(client) -> None:
    """
    List Microsoft Purview Glossary Terms and inspect
    the first returned object.
    """
    terms = client.glossary_terms.list()

    print("Collection type:")
    print(type(terms))

    print()
    print(
        "Glossary Term count:",
        len(terms),
    )

    if not terms:
        print()
        print("No Glossary Terms were returned.")
        return

    first_term = terms[0]

    print()
    print("First item type:")
    print(type(first_term))

    print()
    print("First Glossary Term properties:")
    print("ID:", first_term.id)
    print("Name:", first_term.name)
    print(
        "Description:",
        first_term.description,
    )
    print("Status:", first_term.status)
    print(
        "Domain ID:",
        first_term.domain_id,
    )

    print()
    print(
        "First Glossary Term as a dictionary:"
    )
    print(first_term.to_dict())
```

Call the function using:

```python
list_glossary_terms(client)
```

The complete runnable example is available at:

```text
examples/get_properties/list_glossary_terms.py
```

The supplied example confirms that `list()` returns a list, inspects the first Glossary Term model, reads its main properties, and converts it to a dictionary. :contentReference[oaicite:1]{index=1}

---

### Accessing Individual Glossary Terms

Because `terms` is a list, you can iterate over all returned Glossary Terms:

```python
for term in terms:
    print("ID:", term.id)
    print("Name:", term.name)
    print(
        "Description:",
        term.description,
    )
    print("Status:", term.status)
    print(
        "Domain ID:",
        term.domain_id,
    )
    print()
```

You can also access an individual item by index:

```python
first_term = terms[0]

print(first_term.id)
print(first_term.name)
print(first_term.status)
```

!!! warning "Check the List Before Accessing an Item"

    Do not access `terms[0]` before confirming that the list contains at least one item.

    If no Glossary Terms are returned, Python will raise:

    ```text
    IndexError: list index out of range
    ```

    Use:

    ```python
    if not terms:
        print("No Glossary Terms were returned.")
        return
    ```

---

### Converting a Glossary Term to a Dictionary

Glossary Term model objects provide a `to_dict()` method:

```python
term_dict = terms[0].to_dict()

print(term_dict)
```

This is useful when:

- Inspecting the complete API response
- Exporting Glossary Terms
- Serializing model data
- Comparing term properties
- Preparing results for additional processing

---

## Update a Glossary Term

Use `client.glossary_terms.update()` to update an existing Glossary Term.

The operation requires the unique Glossary Term ID.

---

### Update Values

```python
GLOSSARY_TERM_ID = (
    "22222222-2222-2222-2222-222222222222"
)

NEW_NAME = (
    "SDK Test Glossary Term Updated"
)

NEW_DESCRIPTION = (
    "Glossary term updated by the "
    "Purview Unified SDK example."
)
```

!!! danger "Replace the Example Glossary Term ID"

    The value shown for `GLOSSARY_TERM_ID` is a masked example.

    Replace it with the ID of an existing Glossary Term in your own Microsoft Purview environment.

    Using an invalid or nonexistent ID will cause the update operation to fail.

You may store the ID in `.env`:

```text
PURVIEW_GLOSSARY_TERM_ID=22222222-2222-2222-2222-222222222222
```

Then load it using:

```python
GLOSSARY_TERM_ID = os.environ[
    "PURVIEW_GLOSSARY_TERM_ID"
]
```

---

### Update Example

```python
def update_glossary_term(client) -> None:
    """
    Update an existing Microsoft Purview Glossary Term.
    """
    print("=" * 80)
    print("Glossary Term - Update")
    print("=" * 80)
    print(
        "Glossary Term ID:",
        GLOSSARY_TERM_ID,
    )
    print("New name:", NEW_NAME)
    print()

    glossary_term = (
        client.glossary_terms.update(
            term_id=GLOSSARY_TERM_ID,
            name=NEW_NAME,
            description=NEW_DESCRIPTION,
        )
    )

    print("=" * 80)
    print("Updated Glossary Term")
    print("=" * 80)
    print("ID:", glossary_term.id)
    print("Name:", glossary_term.name)
    print(
        "Description:",
        glossary_term.description,
    )
    print(
        "Status:",
        glossary_term.status,
    )
    print(
        "Domain ID:",
        glossary_term.domain_id,
    )
```

Call the function using:

```python
update_glossary_term(client)
```

The complete runnable example is available at:

```text
examples/glossary_terms/update_glossary_term.py
```

The example updates the term name and description, then prints the returned ID, name, description, status, and Domain ID. :contentReference[oaicite:2]{index=2}

---

### Partial Updates

Only the supplied fields are updated.

For example, to update only the description:

```python
glossary_term = (
    client.glossary_terms.update(
        term_id=GLOSSARY_TERM_ID,
        description=(
            "Updated Glossary Term description."
        ),
    )
)
```

To update only the name:

```python
glossary_term = (
    client.glossary_terms.update(
        term_id=GLOSSARY_TERM_ID,
        name="Updated Business Term",
    )
)
```

Do not replace existing values with empty strings unless that behavior has been verified for the selected Microsoft Purview API version.

---

## Delete a Glossary Term

Use `client.glossary_terms.delete()` to delete an existing Glossary Term.

The operation requires the unique Glossary Term ID.

---

### Delete Value

```python
GLOSSARY_TERM_ID = (
    "22222222-2222-2222-2222-222222222222"
)
```

!!! danger "Replace the Example Glossary Term ID"

    Replace the masked value with the ID of the Glossary Term that you intend to delete.

    Carefully verify the ID before running the operation.

---

### Delete Example

```python
def delete_glossary_term(client) -> None:
    """
    Delete an existing Microsoft Purview Glossary Term.
    """
    print("=" * 80)
    print("Glossary Term - Delete")
    print("=" * 80)
    print(
        "Glossary Term ID:",
        GLOSSARY_TERM_ID,
    )
    print()

    client.glossary_terms.delete(
        GLOSSARY_TERM_ID
    )

    print("=" * 80)
    print("Glossary Term Deleted")
    print("=" * 80)
    print(
        "Deleted Glossary Term ID:",
        GLOSSARY_TERM_ID,
    )
```

Call the function using:

```python
delete_glossary_term(client)
```

The complete runnable example is available at:

```text
examples/glossary_terms/delete_glossary_term.py
```

The example deletes the specified term and prints the deleted Glossary Term ID after the request completes. :contentReference[oaicite:3]{index=3}

!!! danger "Deletion Is Destructive"

    Deleting a Glossary Term is a destructive operation.

    Before deleting a term:

    - Confirm that the Glossary Term ID is correct.
    - Review all existing relationships.
    - Check whether the term is linked to Data Assets.
    - Check whether the term is linked to Data Columns.
    - Check whether the term is linked to Critical Data Elements.
    - Test deletion in a non-production environment whenever possible.

    Removing a Glossary Term may affect the governance context shown for related resources.

---

## Glossary Term Model

Create and update operations return a Glossary Term model object. The list operation returns a list of these objects.

Common properties demonstrated by the examples include:

| Property | Description |
|---|---|
| `id` | Unique identifier of the Glossary Term. |
| `name` | Display name of the term. |
| `description` | Business definition or description. |
| `status` | Current publication or lifecycle status. |
| `domain_id` | ID of the containing Business Domain. |
| `to_dict()` | Converts the model object into a dictionary. |

Example:

```python
print(term.id)
print(term.name)
print(term.description)
print(term.status)
print(term.domain_id)
print(term.to_dict())
```

Not every endpoint necessarily returns every property. Use `to_dict()` when you need to inspect the complete response.

---

## Glossary Terms and Relationships

Glossary Terms can provide business meaning to technical and governance resources.

Supported relationship scenarios include associations with:

- Data Assets
- Data Columns
- Critical Data Elements
- Data Products, where supported by the relevant relationship operation

For example:

```text
Glossary Term
      │
      ├──────────────► Data Asset
      │
      ├──────────────► Data Column
      │
      └──────────────► Critical Data Element
```

The availability and direction of each relationship depend on the Microsoft Purview Unified Catalog API.

For the complete tested support matrix, see:

[Relationship Matrix](../api_reference/relationship_matrix.md)

---

## Complete Operation Pattern

A typical Glossary Term workflow is:

```text
Create a Business Domain
        ↓
Create a Glossary Term in that Domain
        ↓
Record the returned Glossary Term ID
        ↓
List and inspect the term
        ↓
Link it to Assets, Columns, or CDEs
        ↓
Update its definition
        ↓
Delete it when it is no longer required
```

The returned Glossary Term ID is required for many later operations, including:

- Updating the term
- Deleting the term
- Linking the term to a Data Asset
- Linking the term to a Data Column
- Linking the term to a Critical Data Element

---

## Example Files

| File | Purpose |
|---|---|
| `examples/glossary_terms/create_glossary_term.py` | Creates a Glossary Term and prints its returned properties. |
| `examples/get_properties/list_glossary_terms.py` | Lists Glossary Terms and inspects the first returned model object. |
| `examples/glossary_terms/update_glossary_term.py` | Updates the name and description of an existing term. |
| `examples/glossary_terms/delete_glossary_term.py` | Deletes an existing Glossary Term. |

---

## Common Issues

### Invalid Business Domain ID

A create operation can fail when the supplied `domain_id`:

- Does not exist
- Belongs to another environment
- Was copied incorrectly
- Is inaccessible to the authenticated identity

Verify the Business Domain ID before retrying.

### No Glossary Terms Returned

The list operation may return an empty list:

```python
terms = client.glossary_terms.list()

if not terms:
    print("No Glossary Terms were returned.")
```

This may mean that no Glossary Terms exist or that the authenticated identity cannot access them.

### Glossary Term Not Found

Update and delete operations can fail when the supplied ID:

- Does not exist
- Has already been deleted
- Belongs to another environment
- Was entered incorrectly

### Unauthorized or Forbidden

If the request returns `401 Unauthorized` or `403 Forbidden`, first verify that the SDK is using the Microsoft Purview **Unified Catalog** endpoint rather than a classic Purview Data Catalog endpoint.

Then verify that the authenticated user, service principal, or managed identity has permission to manage Glossary Terms.

### Delete Operation Fails

A Glossary Term may be connected to Data Assets, Data Columns, CDEs, or other governance resources.

Review those relationships before retrying deletion.

---

## Next Steps

After creating and managing Glossary Terms, continue with the Critical Data Elements guide.

**Next:** [Critical Data Elements →](cdes.md)