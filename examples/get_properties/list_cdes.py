from purview_api import PurviewClient, PurviewConfig
from dotenv import load_dotenv
import os


load_dotenv()

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:
    cdes = client.cdes.query_models()

    print(type(cdes))
    print("CDE count:", len(cdes))

    if cdes:
        print(type(cdes[0]))
        print()
        print(cdes[0].id)
        print(cdes[0].name)
        print(cdes[0].description)
        print(cdes[0].status)
        print(cdes[0].data_type)
        print(cdes[0].domain_id)

        print()
        print(cdes[0].to_dict())