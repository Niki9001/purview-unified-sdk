# Relationship Matrix

This page summarizes the Microsoft Purview Unified Catalog relationships currently supported and tested by the Purview Unified SDK.

Use this matrix to identify:

- The recommended source resource
- The target entity type
- The SDK method
- Whether the relationship has been tested
- Whether the relationship is direct or indirect

For complete creation and verification examples, see the [Relationships](../user_guide/relationships.md) guide.

---

## Status Definitions

| Status | Meaning |
|---|---|
| **Supported and tested** | The relationship has been successfully created and verified using the SDK. |
| **Supported by helper method** | The SDK provides a dedicated convenience method for the relationship. |
| **Reverse-side tested** | The relationship has been tested from the opposite resource direction. |
| **Indirect** | The association may appear in Microsoft Purview through another connected resource rather than through a direct relationship API. |
| **Not yet tested** | The relationship has not yet been validated with the current SDK examples. |
| **Not directly supported** | No direct relationship operation has been identified. This does not necessarily mean the resources cannot appear associated in Microsoft Purview. |

---

## Relationship Matrix

| Source Resource | Target Resource | Resource Path | Target Entity Type | SDK Operation | Status |
|---|---|---|---|---|---|
| Data Product | Data Asset | `dataProducts` | `DATAASSET` | `relationships.create()` | Supported and tested |
| Data Asset | Data Product | `dataAssets` | `DATAPRODUCT` | `relationships.create()` | Reverse-side tested |
| Data Product | Glossary Term | `dataProducts` | `TERM` | `relationships.create()` | Supported and tested |
| Data Product | Objective | Managed by helper | Managed by helper | `add_objective_to_data_product()` | Supported by helper method |
| Glossary Term | Data Asset | `terms` | `DATAASSET` | `relationships.create()` | Supported and tested |
| Glossary Term | Data Column | `terms` | `DATACOLUMN` | `relationships.create()` | Supported and tested |
| Glossary Term | Critical Data Element | Relationship may be created from the CDE side | `TERM` | `relationships.create()` | Supported and tested from CDE side |
| Critical Data Element | Glossary Term | `criticalDataElements` | `TERM` | `relationships.create()` | Supported and tested |
| Critical Data Element | Data Column | `criticalDataElements` | `DATACOLUMN` | `relationships.create()` | Supported and tested |
| Data Column | Data Asset | `dataColumns` | `DATAASSET` | `relationships.create()` | Supported and tested |
| Data Asset | Data Column | `dataAssets` | `DATACOLUMN` | Relationship read and verification | Supported and tested |
| Data Product | Critical Data Element | — | — | — | No direct relationship provided by Microsoft Purview |
| Critical Data Element | Data Product | — | — | — | No direct relationship provided by Microsoft Purview |
| Data Product | Data Column | — | — | — | No direct relationship provided by Microsoft Purview, but can through Data Asset |
| Data Column | Data Product | — | — | — | No direct relationship provided by Microsoft Purview, but can through Data Asset |
| Objective | Data Product | — | — | Use Data Product helper direction | Supported and tested |
| Data Asset | Glossary Term | — | — | Use Glossary Term source direction | Supported and tested |
| Data Column | Glossary Term | — | — | Use Glossary Term source direction | Supported and tested |

---

## Recommended Creation Directions

When more than one direction may appear possible, use the direction that has been explicitly tested.

| Relationship | Recommended Direction |
|---|---|
| Data Product and Data Asset | Data Product → Data Asset |
| Data Product and Glossary Term | Data Product → Glossary Term |
| Data Product and Objective | Data Product → Objective |
| Glossary Term and Data Asset | Glossary Term → Data Asset |
| Glossary Term and Data Column | Glossary Term → Data Column |
| Glossary Term and CDE | CDE → Glossary Term |
| CDE and Data Column | CDE → Data Column |
| Data Asset and Data Column | Data Column → Data Asset |

!!! warning "Relationship Direction Matters"

    Do not assume that every relationship can be created from either side.

    A relationship may be readable from both resources while only one direction has been confirmed for creation.

    Use the recommended direction unless the reverse direction has been separately tested.

---

## Data Product and Data Asset

### Recommended direction

```text
Data Product
      │
      ▼
Data Asset
```

Configuration:

```python
resource_path = "dataProducts"
entity_type = "DATAASSET"
```

Creation:

```python
relationship = client.relationships.create(
    resource_path="dataProducts",
    resource_id=DATA_PRODUCT_ID,
    entity_type="DATAASSET",
    entity_id=DATA_ASSET_ID,
    relationship_type="Related",
    description=(
        "Data Asset linked to a Data Product."
    ),
)
```

This direction has been tested with duplicate checking and post-creation verification. :contentReference[oaicite:0]{index=0}

The reverse direction has also been investigated using:

```python
resource_path = "dataAssets"
entity_type = "DATAPRODUCT"
```

The reverse-side example reads and compares the association from both endpoints. :contentReference[oaicite:1]{index=1}

---

## Data Product and Glossary Term

### Recommended direction

```text
Data Product
      │
      ▼
Glossary Term
```

Configuration:

```python
resource_path = "dataProducts"
entity_type = "TERM"
```

Creation:

```python
relationship = client.relationships.create(
    resource_path="dataProducts",
    resource_id=DATA_PRODUCT_ID,
    entity_type="TERM",
    entity_id=GLOSSARY_TERM_ID,
    relationship_type="Related",
    description=(
        "Glossary Term linked to a Data Product."
    ),
)
```

This relationship has been tested with duplicate prevention and final verification. :contentReference[oaicite:2]{index=2}

---

## Data Product and Objective

### Recommended direction

```text
Data Product
      │
      ▼
Objective
```

Use the dedicated helper method:

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

The SDK helper hides the lower-level resource-path and entity-type configuration. :contentReference[oaicite:3]{index=3}

!!! note "Use the Helper Method"

    Prefer `add_objective_to_data_product()` over the generic `create()` method when connecting an Objective to a Data Product.

---

## Glossary Term and Data Asset

### Recommended direction

```text
Glossary Term
      │
      ▼
Data Asset
```

Configuration:

```python
resource_path = "terms"
entity_type = "DATAASSET"
```

This direction has been tested with an existing-relationship check and post-creation verification. :contentReference[oaicite:4]{index=4}

---

## Glossary Term and Data Column

### Recommended direction

```text
Glossary Term
      │
      ▼
Data Column
```

Configuration:

```python
resource_path = "terms"
entity_type = "DATACOLUMN"
```

This direction has been tested with the outer Unified Catalog Data Column object ID. :contentReference[oaicite:5]{index=5}

!!! warning "Use the Unified Catalog Column ID"

    Use the outer Unified Catalog object ID for the Data Column.

    Do not substitute a nested source-system column identifier such as `source.columnId` unless the API operation explicitly requires it.

---

## Critical Data Element and Glossary Term

### Recommended direction

```text
Critical Data Element
          │
          ▼
   Glossary Term
```

Configuration:

```python
resource_path = "criticalDataElements"
entity_type = "TERM"
```

This relationship has been tested from the Critical Data Element side. :contentReference[oaicite:6]{index=6}

---

## Critical Data Element and Data Column

### Recommended direction

```text
Critical Data Element
          │
          ▼
     Data Column
```

Configuration:

```python
resource_path = "criticalDataElements"
entity_type = "DATACOLUMN"
```

The tested example:

1. Reads existing Data Column relationships.
2. Checks for the target column ID.
3. Creates the relationship when necessary.
4. Reads the relationships again.
5. Confirms that the Data Column is present. :contentReference[oaicite:7]{index=7}

---

## Data Column and Data Asset

### Recommended direction

```text
Data Column
      │
      ▼
Data Asset
```

Configuration:

```python
resource_path = "dataColumns"
entity_type = "DATAASSET"
```

The tested example verifies the association from both directions:

```text
Data Column → Data Asset
Data Asset  → Data Column
```

This confirms whether the relationship is visible from both resource endpoints. :contentReference[oaicite:8]{index=8}

---

## Direct and Indirect Relationships

Not every association shown in Microsoft Purview is created through a direct relationship endpoint.

For example, a Critical Data Element may appear associated with a Data Product through a shared Data Asset or Data Column.

```text
Critical Data Element
          │
          ▼
Data Column or Data Asset
          │
          ▼
     Data Product
```

This is an **indirect relationship**.

A direct operation such as the following has not been established:

```text
Data Product → Critical Data Element
```

However, the CDE may still appear under the Data Product when both resources are connected through the same technical metadata.

!!! note "Not Directly Supported Does Not Mean Unrelated"

    A matrix entry marked **Not directly supported** means that no direct create operation has been identified.

    Microsoft Purview may still infer or display the association through related resources.

---

## Relationship Visibility

The following situations are possible after a relationship is created:

| Result | Meaning |
|---|---|
| Visible from both sides | Both resource endpoints return the relationship. |
| Visible from the source side only | The create direction returns the relationship, but the reverse endpoint does not yet expose it. |
| Returned by API but not visible in UI | The Unified Catalog interface may not have refreshed yet. |
| Visible indirectly | Microsoft Purview derives the association through another resource. |
| Duplicate entries returned | The relationship may have been created more than once. |

Always verify through the API before relying only on the Microsoft Purview interface.

---

## Generic Configuration Reference

| Source Resource | `resource_path` |
|---|---|
| Data Product | `dataProducts` |
| Data Asset | `dataAssets` |
| Data Column | `dataColumns` |
| Glossary Term | `terms` |
| Critical Data Element | `criticalDataElements` |

Common target entity types include:

| Target Resource | `entity_type` |
|---|---|
| Data Product | `DATAPRODUCT` |
| Data Asset | `DATAASSET` |
| Data Column | `DATACOLUMN` |
| Glossary Term | `TERM` |

The Objective relationship uses a dedicated SDK helper and does not require callers to provide these generic values directly.

---

## Generic Relationship Operation

Most directly supported relationships use:

```python
relationship = client.relationships.create(
    resource_path=SOURCE_RESOURCE_PATH,
    resource_id=SOURCE_RESOURCE_ID,
    entity_type=TARGET_ENTITY_TYPE,
    entity_id=TARGET_ENTITY_ID,
    relationship_type="Related",
    description=(
        "Relationship created by the "
        "Purview Unified SDK."
    ),
)
```

Existing relationships can be read using:

```python
response = client.relationships.list_raw(
    resource_path=SOURCE_RESOURCE_PATH,
    resource_id=SOURCE_RESOURCE_ID,
    entity_type=TARGET_ENTITY_TYPE,
)
```

For a complete duplicate-safe creation workflow, see the [Relationships](../user_guide/relationships.md) guide.

---

## Validation Requirements

A relationship should be marked **Supported and tested** only after the following steps succeed:

```text
Read existing relationships
        ↓
Confirm the target is not already present
        ↓
Create the relationship
        ↓
Read the relationships again
        ↓
Confirm the target entity ID
        ↓
Verify from the reverse side when applicable
```

A successful create response alone does not prove that the relationship is fully visible from every resource endpoint.

---

## Updating This Matrix

When a new relationship is tested:

1. Add it to the main matrix.
2. Record the tested source direction.
3. Record the `resource_path`.
4. Record the target `entity_type`.
5. Identify whether a generic or dedicated SDK method was used.
6. Verify the relationship after creation.
7. Note whether it is visible from the reverse side.
8. Add or link the corresponding example file.

Avoid marking a relationship as supported based only on assumptions about resource types.

---

## Related Documentation

- [Relationships](../user_guide/relationships.md)
- [Data Map](../user_guide/data_map.md)
- [Data Products](../user_guide/data_products.md)
- [Glossary](../user_guide/glossary.md)
- [Critical Data Elements](../user_guide/cdes.md)
- [Objectives and Key Results](../user_guide/okrs.md)