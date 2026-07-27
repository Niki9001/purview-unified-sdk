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
    relationships = client.relationships.list(
        resource_path="dataProducts",
        resource_id=DATA_PRODUCT_ID,
        entity_type="DATAASSET",
    )

    print("Relationship count:", len(relationships))

    for relationship in relationships:
        print(relationship.to_dict())