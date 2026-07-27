from purview import PurviewClient, PurviewConfig
import os

from dotenv import load_dotenv
load_dotenv()


DATA_PRODUCT_ID = os.environ["PURVIEW_DATA_PRODUCT_ID"]


config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:
    assets = client.navigator.get_data_product_assets(
        DATA_PRODUCT_ID
    )

    print("Asset count:", len(assets))

    for asset in assets:
        print()
        print("Asset ID:", asset.id)
        print("Asset name:", asset.name)
        print("Asset type:", asset.type)

        source = asset.source

        print("Source asset type:", source.get("assetType"))
        print("FQN:", source.get("fqn"))

        schema = asset.raw.get("schema", [])

        print(
            "Column count:",
            len(schema) if isinstance(schema, list) else 0,
        )