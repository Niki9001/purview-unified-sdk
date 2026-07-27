from pprint import pprint
import os
from dotenv import load_dotenv


from purview import PurviewClient, PurviewConfig


load_dotenv()

DATA_ASSET_ID = os.environ["PURVIEW_DATA_ASSET_ID"]


config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:
    asset = client.data_assets.get(
        DATA_ASSET_ID,
        include_extended_properties=True,
        include_lineage=False,
    )

    print("=" * 80)
    print("Basic asset information")
    print("=" * 80)

    print("Object type:", type(asset))
    print("ID:", asset.id)
    print("Name:", asset.name)
    print("Unified Catalog type:", asset.type)
    print("Description:", asset.description)
    print("Domain ID:", asset.domain_id)
    print("Open URL:", asset.open_in_url)

    print()
    print("=" * 80)
    print("Source information")
    print("=" * 80)

    print("Source asset type:", asset.source_type)
    print("Source system type:", asset.source_system_type)
    print("Source account:", asset.account_name)
    print("Source asset ID:", asset.source_asset_id)
    print("FQN:", asset.fqn)
    print("Qualified name:", asset.qualified_name)

    print()
    print("=" * 80)
    print("System information")
    print("=" * 80)

    print("Created at:", asset.created_at)
    print("Last modified at:", asset.last_modified_at)
    print("Provisioning state:", asset.provisioning_state)
    print("Is migrated:", asset.is_migrated)

    print()
    print("=" * 80)
    print("Schema information")
    print("=" * 80)

    print("Column count:", asset.column_count)

    print("\nFirst 10 columns:")

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

    column = asset.get_column("BUKRS")

    if column is None:
        print("Column BUKRS was not found.")
    else:
        pprint(column)

    print()
    print("=" * 80)
    print("Known model fields")
    print("=" * 80)

    pprint(asset.to_dict())

    print()
    print("=" * 80)
    print("Raw API keys")
    print("=" * 80)

    pprint(list(asset.raw.keys()))

    print()
    print("=" * 80)
    print("Raw schema count")
    print("=" * 80)

    raw_schema = asset.raw.get("schema", [])

    if isinstance(raw_schema, list):
        print("Raw schema count:", len(raw_schema))
    else:
        print("Raw schema is not a list.")