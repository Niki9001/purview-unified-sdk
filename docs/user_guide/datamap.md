# Data Map

Microsoft Purview Data Map contains technical metadata about discovered and registered data resources.

In the Purview Unified SDK, Data Map resources are represented primarily through:

- Data Assets
- Data Columns
- Source-system metadata
- Schema information
- Raw API responses

The Data Map client allows you to retrieve a Data Asset by ID and inspect its technical properties through a Python model.

A typical resource structure is:

```text
Source System
      │
      ▼
 Data Asset
      │
      ▼
 Data Column
```

Data Map resources may also participate in governance relationships:

```text
Data Product
      │
      ▼
 Data Asset
      │
      ▼
 Data Column
      │
      ▼
Critical Data Element
```

This guide focuses on retrieving and inspecting Data Map resources.

For creating relationships between Data Map and governance resources, see [Relationships](relationships.md).

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

You must also know the Unified Catalog ID of the Data Asset that you want to retrieve.

---

## Data Asset ID

The complete example reads the Data Asset ID from the `.env` file:

```python
DATA_ASSET_ID = os.environ[
    "PURVIEW_DATA_ASSET_ID"
]
```

Add the value to `.env`:

```text
PURVIEW_DATA_ASSET_ID=11111111-1111-1111-1111-111111111111
```

!!! danger "Replace the Example Data Asset ID"

    Replace the example value with the ID of an existing Data Asset in your Microsoft Purview environment.

    The Data Asset ID must belong to the same Microsoft Purview environment used by the authenticated client.

---

## Get a Data Asset

Use `client.data_assets.get()` to retrieve a single Data Asset.

```python
asset = client.data_assets.get(
    DATA_ASSET_ID,
    include_extended_properties=True,
    include_lineage=False,
)
```

The method returns a Data Asset model rather than an unprocessed dictionary.

You can therefore access properties directly:

```python
print(asset.id)
print(asset.name)
print(asset.description)
```

---

## Retrieval Options

The example passes two optional arguments:

```python
include_extended_properties=True
include_lineage=False
```

### Extended Properties

```python
include_extended_properties=True
```

Requests additional Data Asset properties from the API.

These properties may include technical source information, schema details, and other metadata returned for the selected asset.

### Lineage

```python
include_lineage=False
```

The example does not request lineage information.

Set this according to the behavior supported by your SDK and Microsoft Purview environment.

---

## Basic Asset Information

The Data Asset model exposes common Unified Catalog properties:

```python
print("Object type:", type(asset))
print("ID:", asset.id)
print("Name:", asset.name)
print(
    "Unified Catalog type:",
    asset.type,
)
print(
    "Description:",
    asset.description,
)
print(
    "Domain ID:",
    asset.domain_id,
)
print(
    "Open URL:",
    asset.open_in_url,
)
```

Common properties include:

| Property | Description |
|---|---|
| `id` | Unique Unified Catalog ID of the Data Asset. |
| `name` | Display name of the asset. |
| `type` | Unified Catalog resource type. |
| `description` | Description of the asset. |
| `domain_id` | ID of the Business Domain associated with the asset. |
| `open_in_url` | URL that may be used to open the asset in Microsoft Purview. |

---

## Inspect the Returned Model Type

You can inspect the Python object returned by the SDK:

```python
print(
    "Object type:",
    type(asset),
)
```

This helps confirm that the SDK returned a model object instead of a raw JSON dictionary.

Because the result is a model, properties can be accessed using attribute notation:

```python
asset.name
asset.description
asset.domain_id
```

Instead of:

```python
asset["name"]
asset["description"]
asset["domainId"]
```

---

## Source Information

Data Assets may contain metadata describing the source platform and source object.

```python
print(
    "Source asset type:",
    asset.source_type,
)
print(
    "Source system type:",
    asset.source_system_type,
)
print(
    "Source account:",
    asset.account_name,
)
print(
    "Source asset ID:",
    asset.source_asset_id,
)
print(
    "FQN:",
    asset.fqn,
)
print(
    "Qualified name:",
    asset.qualified_name,
)
```

Common source properties include:

| Property | Description |
|---|---|
| `source_type` | Source asset type returned by Microsoft Purview. |
| `source_system_type` | Type of source system containing the asset. |
| `account_name` | Source account or connection name. |
| `source_asset_id` | Identifier of the object in the source system. |
| `fqn` | Fully qualified name of the source asset. |
| `qualified_name` | Qualified name returned for the asset. |

These values can help distinguish between:

```text
Unified Catalog identity
```

and:

```text
Source-system identity
```

The two identifiers may not be the same.

---

## Unified Catalog ID and Source Asset ID

A Data Asset may expose more than one identifier.

```text
Unified Catalog ID
        │
        └── asset.id

Source-system ID
        │
        └── asset.source_asset_id
```

Use `asset.id` when an SDK operation requires the Unified Catalog Data Asset ID.

Use source-system identifiers only when the specific API or operation explicitly requires them.

!!! warning "Do Not Mix Resource IDs"

    A Unified Catalog object ID and a source-system asset ID may identify the same logical asset in different systems, but they are not necessarily interchangeable.

    Relationship operations generally require the Unified Catalog resource ID expected by the API.

---

## System Information

The Data Asset model also exposes system-managed properties:

```python
print(
    "Created at:",
    asset.created_at,
)
print(
    "Last modified at:",
    asset.last_modified_at,
)
print(
    "Provisioning state:",
    asset.provisioning_state,
)
print(
    "Is migrated:",
    asset.is_migrated,
)
```

Common properties include:

| Property | Description |
|---|---|
| `created_at` | Date and time when the asset was created or registered. |
| `last_modified_at` | Date and time when the asset was last modified. |
| `provisioning_state` | Current provisioning state returned by the API. |
| `is_migrated` | Indicates whether the asset is marked as migrated. |

The exact values depend on the API response for the selected asset.

---

## Schema Information

A Data Asset may include schema information describing its columns.

The number of columns is available through:

```python
print(
    "Column count:",
    asset.column_count,
)
```

The returned columns can be accessed through:

```python
asset.columns
```

---

## List Data Columns

The example prints the first ten columns:

```python
for column in asset.columns[:10]:
    print(
        f"- {column.get('name')} "
        f"({column.get('type')}): "
        f"{column.get('description')}"
    )
```

Each column entry may contain values such as:

```python
column.get("name")
column.get("type")
column.get("description")
```

Using `.get()` avoids raising a `KeyError` when an optional value is missing.

---

## Print All Columns

To print every returned column:

```python
for column in asset.columns:
    print(
        "Name:",
        column.get("name"),
    )
    print(
        "Type:",
        column.get("type"),
    )
    print(
        "Description:",
        column.get("description"),
    )
    print()
```

For assets with large schemas, consider limiting the output:

```python
for column in asset.columns[:10]:
    ...
```

---

## Find a Column by Name

The Data Asset model provides a convenience method for locating a column by name:

```python
column = asset.get_column(
    "BUKRS"
)
```

Then check whether the column was found:

```python
if column is None:
    print(
        "Column BUKRS was not found."
    )
else:
    pprint(column)
```

This avoids writing a manual loop each time a specific column is needed.

Without the convenience method, the equivalent logic would be similar to:

```python
column = next(
    (
        item
        for item in asset.columns
        if item.get("name") == "BUKRS"
    ),
    None,
)
```

Using `asset.get_column()` is clearer and easier to reuse.

---

## Column Lookup Result

`asset.get_column()` returns:

- The matching column information when found
- `None` when no matching column is found

Always check for `None` before accessing the result:

```python
column = asset.get_column(
    "BUKRS"
)

if column is not None:
    print(
        column.get("name")
    )
```

!!! note "Column Name Matching"

    Supply the column name expected by the Data Asset model.

    A column may not be found when the spelling, formatting, or letter case differs from the value stored in Microsoft Purview.

---

## Convert the Model to a Dictionary

Use `asset.to_dict()` to convert the known model fields into a Python dictionary:

```python
asset_dictionary = (
    asset.to_dict()
)

pprint(
    asset_dictionary
)
```

This is useful when:

- Exporting asset information
- Serializing results
- Logging model properties
- Passing data to another Python function
- Comparing multiple assets

Example:

```python
print(
    asset.to_dict()
)
```

---

## Model Fields and Raw Response

The SDK provides two different views of the Data Asset:

```text
Data Asset model
        │
        └── asset.to_dict()

Raw API response
        │
        └── asset.raw
```

These views serve different purposes.

### Model View

```python
asset.to_dict()
```

Provides the fields recognized and exposed by the SDK model.

### Raw API View

```python
asset.raw
```

Provides access to the original response data retained by the model.

This can be useful when Microsoft Purview returns fields that have not yet been added as formal SDK properties.

---

## Inspect Raw API Keys

To see which top-level keys were returned by the API:

```python
pprint(
    list(
        asset.raw.keys()
    )
)
```

This can help during:

- API investigation
- SDK development
- Troubleshooting
- Model expansion
- Microsoft Purview response changes

!!! warning "Prefer Model Properties for Normal Use"

    Use model properties such as `asset.name`, `asset.columns`, and `asset.domain_id` for ordinary SDK code.

    Use `asset.raw` mainly when investigating fields that are not yet represented by the model.

    Raw response structures may be less convenient and may change independently of the SDK model interface.

---

## Inspect the Raw Schema

The raw response may contain a `schema` value:

```python
raw_schema = asset.raw.get(
    "schema",
    [],
)
```

Validate the value before using it:

```python
if isinstance(raw_schema, list):
    print(
        "Raw schema count:",
        len(raw_schema),
    )
else:
    print(
        "Raw schema is not a list."
    )
```

This check prevents code from incorrectly assuming that the API always returns a list.

---

## Complete Example

The following example retrieves one Data Asset and displays its primary technical metadata.

```python
from pprint import pprint
import os

from dotenv import load_dotenv

from purview import (
    PurviewClient,
    PurviewConfig,
)


load_dotenv()


DATA_ASSET_ID = os.environ[
    "PURVIEW_DATA_ASSET_ID"
]


def main() -> None:
    """
    Retrieve and inspect a Microsoft Purview
    Data Asset.
    """
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
        asset = client.data_assets.get(
            DATA_ASSET_ID,
            include_extended_properties=True,
            include_lineage=False,
        )

    print("=" * 80)
    print("Basic asset information")
    print("=" * 80)

    print(
        "Object type:",
        type(asset),
    )
    print(
        "ID:",
        asset.id,
    )
    print(
        "Name:",
        asset.name,
    )
    print(
        "Unified Catalog type:",
        asset.type,
    )
    print(
        "Description:",
        asset.description,
    )
    print(
        "Domain ID:",
        asset.domain_id,
    )
    print(
        "Open URL:",
        asset.open_in_url,
    )

    print()
    print("=" * 80)
    print("Source information")
    print("=" * 80)

    print(
        "Source asset type:",
        asset.source_type,
    )
    print(
        "Source system type:",
        asset.source_system_type,
    )
    print(
        "Source account:",
        asset.account_name,
    )
    print(
        "Source asset ID:",
        asset.source_asset_id,
    )
    print(
        "FQN:",
        asset.fqn,
    )
    print(
        "Qualified name:",
        asset.qualified_name,
    )

    print()
    print("=" * 80)
    print("System information")
    print("=" * 80)

    print(
        "Created at:",
        asset.created_at,
    )
    print(
        "Last modified at:",
        asset.last_modified_at,
    )
    print(
        "Provisioning state:",
        asset.provisioning_state,
    )
    print(
        "Is migrated:",
        asset.is_migrated,
    )

    print()
    print("=" * 80)
    print("Schema information")
    print("=" * 80)

    print(
        "Column count:",
        asset.column_count,
    )

    print()
    print("First 10 columns:")

    for column in asset.columns[:10]:
        print(
            f"- {column.get('name')} "
            f"({column.get('type')}): "
            f"{column.get('description')}"
        )

    print()
    print("=" * 80)
    print("Column lookup test")
    print("=" * 80)

    column = asset.get_column(
        "BUKRS"
    )

    if column is None:
        print(
            "Column BUKRS was not found."
        )
    else:
        pprint(
            column,
            sort_dicts=False,
        )

    print()
    print("=" * 80)
    print("Known model fields")
    print("=" * 80)

    pprint(
        asset.to_dict(),
        sort_dicts=False,
    )

    print()
    print("=" * 80)
    print("Raw API keys")
    print("=" * 80)

    pprint(
        list(
            asset.raw.keys()
        )
    )

    print()
    print("=" * 80)
    print("Raw schema count")
    print("=" * 80)

    raw_schema = asset.raw.get(
        "schema",
        [],
    )

    if isinstance(raw_schema, list):
        print(
            "Raw schema count:",
            len(raw_schema),
        )
    else:
        print(
            "Raw schema is not a list."
        )


if __name__ == "__main__":
    main()
```

The original runnable example retrieves a Data Asset, prints its catalog and source metadata, examines its columns, tests `get_column()`, converts the model with `to_dict()`, and inspects the retained raw response. :contentReference[oaicite:0]{index=0}

---

## Data Asset Model

The example demonstrates the following Data Asset properties and methods:

| Property or Method | Description |
|---|---|
| `id` | Unified Catalog Data Asset ID. |
| `name` | Asset name. |
| `type` | Unified Catalog resource type. |
| `description` | Asset description. |
| `domain_id` | Associated Business Domain ID. |
| `open_in_url` | URL for opening the asset. |
| `source_type` | Source asset type. |
| `source_system_type` | Source platform type. |
| `account_name` | Source account name. |
| `source_asset_id` | Source-system asset ID. |
| `fqn` | Fully qualified name. |
| `qualified_name` | Qualified asset name. |
| `created_at` | Creation timestamp. |
| `last_modified_at` | Last modification timestamp. |
| `provisioning_state` | Provisioning state. |
| `is_migrated` | Migration indicator. |
| `column_count` | Number of returned columns. |
| `columns` | Returned schema column collection. |
| `get_column(name)` | Finds a column by name. |
| `to_dict()` | Converts known model fields to a dictionary. |
| `raw` | Retained raw API response. |

---

## Data Assets and Relationships

A Data Asset can participate in relationships with other Microsoft Purview resources.

Examples include:

```text
Data Product
      │
      ▼
 Data Asset
```

```text
Glossary Term
      │
      ▼
 Data Asset
```

```text
Data Asset
      │
      ▼
 Data Column
```

The Data Map guide explains how to retrieve and inspect these technical resources.

The Relationships guide explains how to create and validate associations between them.

See [Relationships](relationships.md).

---

## Data Columns and Relationships

A Data Column can also participate in governance relationships:

```text
Glossary Term
      │
      ▼
 Data Column
```

```text
Critical Data Element
      │
      ▼
 Data Column
```

When creating Data Column relationships, use the Unified Catalog Data Column ID required by the relationship API.

Do not assume that a nested source-system column identifier is interchangeable with the outer Unified Catalog object ID.

---

## Common Issues

### Data Asset Not Found

Verify that:

- The Data Asset ID exists.
- The ID belongs to the correct Microsoft Purview environment.
- The authenticated identity can view the asset.
- The ID is the Unified Catalog Data Asset ID expected by the operation.

---

### Empty Column List

An asset may return no columns when:

- No schema information is available.
- Extended properties were not returned.
- The selected asset type does not expose columns.
- The authenticated identity cannot access the full metadata.
- The source metadata has not been populated.

Check:

```python
print(
    asset.column_count
)
print(
    len(asset.columns)
)
```

---

### Column Not Found

`asset.get_column()` returns `None` when the requested column cannot be found.

```python
column = asset.get_column(
    "COLUMN_NAME"
)

if column is None:
    print(
        "Column was not found."
    )
```

Verify the column name against:

```python
for item in asset.columns:
    print(
        item.get("name")
    )
```

---

### Missing Optional Properties

Some properties may be `None` when the API does not return a value.

For example:

```python
print(
    asset.description
)
```

may display:

```text
None
```

This does not necessarily indicate an SDK error.

It may mean that the property is not populated for the selected Data Asset.

---

### Raw Schema Is Not a List

Do not assume the raw `schema` field always contains a list.

Use:

```python
raw_schema = asset.raw.get(
    "schema",
    [],
)

if isinstance(raw_schema, list):
    ...
```

---

### Incorrect ID Type

Do not confuse:

```text
asset.id
```

with:

```text
asset.source_asset_id
```

The first is the Unified Catalog asset ID exposed by the SDK model.

The second identifies the object in its originating source context.

Use the identifier required by the specific SDK operation.

---

### Unauthorized or Forbidden

If the request returns `401 Unauthorized` or `403 Forbidden`, first verify that the SDK is using the Microsoft Purview **Unified Catalog** endpoint.

Then verify that the authenticated user, service principal, or managed identity has permission to read the selected Data Asset.

---

## Recommended Inspection Workflow

Use the following workflow when investigating a Data Asset:

```text
Obtain the Unified Catalog Data Asset ID
        ↓
Retrieve the Data Asset
        ↓
Inspect basic properties
        ↓
Inspect source information
        ↓
Review schema and columns
        ↓
Look up specific columns
        ↓
Inspect the model dictionary
        ↓
Use the raw response only when needed
```

---

## Example File

| File | Purpose |
|---|---|
| `examples/get_properties/get_data_asset.py` | Retrieves and inspects a Data Asset, its source metadata, schema, model fields, and raw API response. |

---

## Next Steps

Continue with the Relationships guide to connect Data Assets and Data Columns to governance resources.

**Next:** [Relationships →](relationships.md)