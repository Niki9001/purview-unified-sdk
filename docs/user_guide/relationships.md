# Relationships

Relationships connect governance and technical resources in Microsoft Purview Unified Catalog.

For example, a Data Product can be associated with Data Assets, Glossary Terms, and Objectives. A Glossary Term can be connected to Data Assets, Data Columns, and Critical Data Elements.

The Purview Unified SDK provides a generic Relationship client for reading and creating supported relationships.

---

## Relationship Model

A relationship is created from a **source resource** to a **target entity**.

```text
Source Resource
        │
        ▼
Target Entity
```

For example:

```text
Data Product
        │
        ▼
Data Asset
```

The generic relationship operation requires:

| Parameter | Description |
|---|---|
| `resource_path` | API path representing the source resource type. |
| `resource_id` | Unique ID of the source resource. |
| `entity_type` | Microsoft Purview entity type of the target resource. |
| `entity_id` | Unique ID of the target resource. |
| `relationship_type` | Relationship classification, commonly `Related`. |
| `description` | Optional description of the relationship. |

---

## Supported Relationship Examples

The SDK includes tested examples for the following relationship directions:

| Source Resource | Target Resource |
|---|---|
| Data Product | Data Asset |
| Data Product | Glossary Term |
| Data Product | Objective |
| Data Asset | Data Product |
| Data Column | Data Asset |
| Glossary Term | Data Asset |
| Glossary Term | Data Column |
| Glossary Term | Critical Data Element |
| Critical Data Element | Glossary Term |
| Critical Data Element | Data Column |

The availability and behavior of a relationship may depend on its direction.

For the complete support and validation status, see the [Relationship Matrix](../api_reference/relationship_matrix.md).

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

You must also know the IDs of both resources involved in the relationship.

!!! danger "Replace All Example Resource IDs"

    Every ID shown in this guide is a masked example.

    Replace the example values with resource IDs from your own Microsoft Purview environment.

    Resource IDs from different tenants or environments cannot be used interchangeably.

---

## Generic Relationship Pattern

Most relationship examples follow the same process:

```text
Read existing relationships
        ↓
Check whether the target already exists
        ↓
Create the relationship
        ↓
Read the relationships again
        ↓
Verify that the target is now present
```

This pattern helps prevent duplicate relationships and confirms that Microsoft Purview accepted the new association.

---

## Read Existing Relationships

Use `client.relationships.list_raw()` to retrieve existing relationships for a source resource.

```python
before_response = client.relationships.list_raw(
    resource_path=RESOURCE_PATH,
    resource_id=SOURCE_RESOURCE_ID,
    entity_type=TARGET_ENTITY_TYPE,
)
```

The raw response commonly contains a `value` list:

```python
before_items = before_response.get(
    "value",
    [],
)
```

Validate the response before processing it:

```python
if not isinstance(before_items, list):
    raise TypeError(
        "Expected response['value'] to be a list."
    )
```

Extract the existing target IDs:

```python
existing_entity_ids = {
    str(item.get("entityId"))
    for item in before_items
    if isinstance(item, dict)
    and item.get("entityId")
}
```

---

## Avoid Duplicate Relationships

Before creating a relationship, check whether the target ID is already present.

```python
if TARGET_ENTITY_ID in existing_entity_ids:
    print(
        "This relationship already exists."
    )
else:
    # Create the relationship.
    ...
```

!!! warning "Check Before Creating"

    Always read the existing relationships before creating a new one.

    Repeated create requests may produce duplicate entries, API errors, or inconsistent visual behavior in Microsoft Purview.

---

## Create a Relationship

Use `client.relationships.create()` for generic relationship creation.

```python
created_relationship = (
    client.relationships.create(
        resource_path=RESOURCE_PATH,
        resource_id=SOURCE_RESOURCE_ID,
        entity_type=TARGET_ENTITY_TYPE,
        entity_id=TARGET_ENTITY_ID,
        relationship_type="Related",
        description=(
            "Relationship created by the "
            "Purview Unified SDK."
        ),
    )
)
```

The returned relationship model can be inspected using:

```python
print(
    created_relationship.to_dict()
)
```

---

## Verify the Relationship

After creation, read the relationships again:

```python
after_response = client.relationships.list_raw(
    resource_path=RESOURCE_PATH,
    resource_id=SOURCE_RESOURCE_ID,
    entity_type=TARGET_ENTITY_TYPE,
)
```

Extract the returned entity IDs:

```python
after_items = after_response.get(
    "value",
    [],
)

after_entity_ids = {
    str(item.get("entityId"))
    for item in after_items
    if isinstance(item, dict)
    and item.get("entityId")
}
```

Then confirm that the target ID is present:

```python
if TARGET_ENTITY_ID in after_entity_ids:
    print(
        "Success: the relationship was created."
    )
else:
    raise RuntimeError(
        "The create request completed, but the "
        "target resource was not found when the "
        "relationships were read again."
    )
```

---

## Complete Generic Example

```python
from pprint import pprint


RESOURCE_PATH = "dataProducts"
SOURCE_RESOURCE_ID = (
    "11111111-1111-1111-1111-111111111111"
)

TARGET_ENTITY_TYPE = "DATAASSET"
TARGET_ENTITY_ID = (
    "22222222-2222-2222-2222-222222222222"
)

RELATIONSHIP_TYPE = "Related"


def add_relationship(client) -> None:
    """
    Create and verify a Microsoft Purview relationship.
    """
    print("=" * 80)
    print("Relationship - Create")
    print("=" * 80)
    print(
        "Source resource ID:",
        SOURCE_RESOURCE_ID,
    )
    print(
        "Target entity ID:",
        TARGET_ENTITY_ID,
    )
    print(
        "Target entity type:",
        TARGET_ENTITY_TYPE,
    )
    print()

    before_response = (
        client.relationships.list_raw(
            resource_path=RESOURCE_PATH,
            resource_id=SOURCE_RESOURCE_ID,
            entity_type=TARGET_ENTITY_TYPE,
        )
    )

    before_items = before_response.get(
        "value",
        [],
    )

    if not isinstance(before_items, list):
        raise TypeError(
            "Expected response['value'] to be a list."
        )

    existing_entity_ids = {
        str(item.get("entityId"))
        for item in before_items
        if isinstance(item, dict)
        and item.get("entityId")
    }

    if TARGET_ENTITY_ID in existing_entity_ids:
        print(
            "The relationship already exists."
        )
        return

    created_relationship = (
        client.relationships.create(
            resource_path=RESOURCE_PATH,
            resource_id=SOURCE_RESOURCE_ID,
            entity_type=TARGET_ENTITY_TYPE,
            entity_id=TARGET_ENTITY_ID,
            relationship_type=RELATIONSHIP_TYPE,
            description=(
                "Relationship created by the "
                "Purview Unified SDK."
            ),
        )
    )

    print()
    print("Relationship creation response:")

    pprint(
        created_relationship.to_dict(),
        sort_dicts=False,
    )

    after_response = (
        client.relationships.list_raw(
            resource_path=RESOURCE_PATH,
            resource_id=SOURCE_RESOURCE_ID,
            entity_type=TARGET_ENTITY_TYPE,
        )
    )

    after_items = after_response.get(
        "value",
        [],
    )

    if not isinstance(after_items, list):
        raise TypeError(
            "Expected response['value'] to be a list."
        )

    after_entity_ids = {
        str(item.get("entityId"))
        for item in after_items
        if isinstance(item, dict)
        and item.get("entityId")
    }

    if TARGET_ENTITY_ID in after_entity_ids:
        print()
        print(
            "Success: the relationship was created."
        )
    else:
        raise RuntimeError(
            "The create request completed, but the "
            "target resource was not found when the "
            "relationships were read again."
        )
```

---

## Data Product to Data Asset

Use the following configuration:

```python
RESOURCE_PATH = "dataProducts"
TARGET_ENTITY_TYPE = "DATAASSET"
```

Example:

```python
created_relationship = (
    client.relationships.create(
        resource_path="dataProducts",
        resource_id=DATA_PRODUCT_ID,
        entity_type="DATAASSET",
        entity_id=DATA_ASSET_ID,
        relationship_type="Related",
        description=(
            "Data Asset linked to a Data Product."
        ),
    )
)
```

The complete example reads the existing Data Asset relationships, avoids duplicate creation, creates the association, and verifies that the Data Asset appears afterward. :contentReference[oaicite:0]{index=0}

---

## Data Product to Glossary Term

Use:

```python
RESOURCE_PATH = "dataProducts"
TARGET_ENTITY_TYPE = "TERM"
```

Example:

```python
created_relationship = (
    client.relationships.create(
        resource_path="dataProducts",
        resource_id=DATA_PRODUCT_ID,
        entity_type="TERM",
        entity_id=GLOSSARY_TERM_ID,
        relationship_type="Related",
        description=(
            "Glossary Term linked to a "
            "Data Product."
        ),
    )
)
```

The tested example checks for an existing term relationship before creating and verifying the new association. :contentReference[oaicite:1]{index=1}

---

## Data Product to Objective

The SDK provides a convenience method for associating an Objective with a Data Product:

```python
relationship = (
    client.relationships
    .add_objective_to_data_product(
        data_product_id=DATA_PRODUCT_ID,
        objective_id=OBJECTIVE_ID,
        relationship_type="Related",
        description=(
            "Links the Data Product to its "
            "governance Objective."
        ),
    )
)
```

Returned properties include:

```python
relationship.entity_id
relationship.relationship_type
relationship.description
```

The complete example uses the dedicated `add_objective_to_data_product()` helper rather than the generic `create()` method. :contentReference[oaicite:2]{index=2}

---

## Glossary Term to Data Asset

Use:

```python
RESOURCE_PATH = "terms"
TARGET_ENTITY_TYPE = "DATAASSET"
```

Example:

```python
created_relationship = (
    client.relationships.create(
        resource_path="terms",
        resource_id=GLOSSARY_TERM_ID,
        entity_type="DATAASSET",
        entity_id=DATA_ASSET_ID,
        relationship_type="Related",
        description=(
            "Data Asset linked to a "
            "Glossary Term."
        ),
    )
)
```

The example checks the current relationships before creating and verifies the Data Asset afterward. :contentReference[oaicite:3]{index=3}

---

## Glossary Term to Data Column

Use:

```python
RESOURCE_PATH = "terms"
TARGET_ENTITY_TYPE = "DATACOLUMN"
```

!!! warning "Use the Unified Catalog Data Column ID"

    Use the outer Microsoft Purview Unified Catalog object ID for the Data Column.

    Do not use a nested source-system column identifier unless it has been confirmed to be the required Unified Catalog resource ID.

The complete example prevents duplicate relationships and verifies that the Data Column appears after creation. :contentReference[oaicite:4]{index=4}

---

## Critical Data Element to Glossary Term

Use:

```python
RESOURCE_PATH = "criticalDataElements"
TARGET_ENTITY_TYPE = "TERM"
```

Example:

```python
created_relationship = (
    client.relationships.create(
        resource_path="criticalDataElements",
        resource_id=CDE_ID,
        entity_type="TERM",
        entity_id=GLOSSARY_TERM_ID,
        relationship_type="Related",
        description=(
            "Glossary Term linked to a CDE."
        ),
    )
)
```

The example reads the existing Glossary Term relationships, avoids duplicates, and verifies the relationship after creation. :contentReference[oaicite:5]{index=5}

---

## Critical Data Element to Data Column

Use:

```python
RESOURCE_PATH = "criticalDataElements"
TARGET_ENTITY_TYPE = "DATACOLUMN"
```

Example:

```python
created_relationship = (
    client.relationships.create(
        resource_path="criticalDataElements",
        resource_id=CDE_ID,
        entity_type="DATACOLUMN",
        entity_id=DATA_COLUMN_ID,
        relationship_type="Related",
        description=(
            "Data Column linked to a CDE."
        ),
    )
)
```

The complete example confirms that the Data Column is not already linked, creates the relationship, and reads the CDE relationships again for final verification. :contentReference[oaicite:6]{index=6}

---

## Data Column to Data Asset

Use:

```python
RESOURCE_PATH = "dataColumns"
TARGET_ENTITY_TYPE = "DATAASSET"
```

This example also verifies the relationship from both directions:

```text
Data Column → Data Asset
Data Asset → Data Column
```

After creation, the example checks whether the association is visible from both the Data Column and Data Asset sides. :contentReference[oaicite:7]{index=7}

---

## Relationship Direction

Relationship direction is important.

For example, these operations may use different source paths and target entity types:

```text
Data Product → Data Asset
Data Asset → Data Product
```

The reverse-side example uses:

```python
resource_path="dataAssets"
entity_type="DATAPRODUCT"
```

It then verifies the relationship from both the Data Asset and Data Product sides. :contentReference[oaicite:8]{index=8}

!!! warning "Do Not Assume Every Relationship Is Symmetric"

    A relationship visible from one resource may not support creation from the opposite direction.

    Always use a relationship direction that has been documented and validated.

    When testing a reverse direction, read the relationship from both sides before concluding that two distinct relationships exist.

---

## Data Product and CDE Relationships

A direct Data Product-to-CDE relationship operation has not been identified.

Instead, Microsoft Purview may display a CDE under a Data Product indirectly when:

1. The CDE is associated with a Data Asset or Data Column.
2. The same Data Asset is associated with the Data Product.
3. Microsoft Purview infers the connection in the Unified Catalog interface.

```text
Critical Data Element
        │
        ▼
Data Asset or Data Column
        │
        ▼
Data Product
```

!!! note "Indirect Relationship"

    `Data Product → CDE` and `CDE → Data Product` are marked as **not directly supported**.

    This does not mean that the CDE cannot appear under the Data Product.

    It means that the visible association is derived through a shared Data Map resource rather than created through a direct relationship API.

---

## Relationship Response

The generic create operation returns a relationship model.

Common properties may include:

```python
relationship.entity_id
relationship.entity_type
relationship.relationship_type
relationship.description
```

The full returned object can be inspected using:

```python
print(
    relationship.to_dict()
)
```

The exact returned fields may vary depending on the source resource, target entity type, and API response.

---

## Example Files

| File | Relationship |
|---|---|
| `data_product_add_assets.py` | Data Product → Data Asset |
| `data_product_add_glossary_terms.py` | Data Product → Glossary Term |
| `data_product_add_okrs.py` | Data Product → Objective |
| `data_asset_add_data_product.py` | Data Asset → Data Product |
| `data_column_add_data_assets.py` | Data Column → Data Asset |
| `glossary_term_add_data_assets.py` | Glossary Term → Data Asset |
| `glossary_term_add_columns.py` | Glossary Term → Data Column |
| `glossary_term_add_cdes.py` | Glossary Term / CDE relationship |
| `cde_add_columns.py` | CDE → Data Column |

---

## Common Issues

### Duplicate Relationship

Read the existing relationships before creating a new one.

```python
if TARGET_ENTITY_ID in existing_entity_ids:
    print("The relationship already exists.")
```

### Incorrect Resource ID

Confirm that the ID belongs to the expected Unified Catalog resource type.

For Data Columns, use the Unified Catalog object ID required by the relationship API.

### Incorrect Entity Type

Entity types are uppercase API values such as:

```text
DATAASSET
DATACOLUMN
DATAPRODUCT
TERM
```

Using an incorrect entity type may return no results or cause the create operation to fail.

### Incorrect Resource Path

Examples include:

```text
dataProducts
dataAssets
dataColumns
terms
criticalDataElements
```

The resource path must represent the source side of the relationship.

### Relationship Created but Not Visible

Microsoft Purview may require time to refresh the Unified Catalog interface.

Verify the relationship through `list_raw()` before relying only on the UI.

### One-Sided Visibility

A relationship may appear from one resource side before appearing from the other side.

Read both directions when the relationship is expected to be bidirectional.

### Unauthorized or Forbidden

If the request returns `401 Unauthorized` or `403 Forbidden`, first confirm that the SDK is using the Microsoft Purview **Unified Catalog** endpoint rather than a classic Purview Data Catalog endpoint.

Then verify that the authenticated identity has permission to manage both resources involved in the relationship.

---

## Recommended Relationship Workflow

Use the following process for production scripts:

```text
Validate the source ID
        ↓
Validate the target ID
        ↓
Read existing relationships
        ↓
Skip if the relationship already exists
        ↓
Create the relationship
        ↓
Read the relationship again
        ↓
Verify from the reverse side when applicable
        ↓
Log the final result
```

---

## Next Steps

Review the complete supported and validated relationship combinations.

**Next:** [Relationship Matrix →](../api_reference/relationship_matrix.md)