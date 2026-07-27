from purview_api import PurviewClient, PurviewConfig
import os
from dotenv import load_dotenv


load_dotenv()

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:
    data_products = client.data_products.list()

    print(type(data_products))
    print("Data Product count:", len(data_products))

    if data_products:
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