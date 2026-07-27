from pprint import pprint

from purview import PurviewClient, PurviewConfig

import os

from dotenv import load_dotenv


load_dotenv()

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

client = PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
)

try:
    result = client.get("/businessdomains")
    pprint(result)
finally:
    client.close()