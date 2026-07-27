from purview import PurviewClient, PurviewConfig

import os

from dotenv import load_dotenv


load_dotenv()

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

client = PurviewClient(config)

print("Base URL:", client.base_url)
print("Domains URL:", client.build_url("/domains"))
print("Terms URL:", client.build_url("terms"))
print(
    "CDE query URL:",
    client.build_url("/criticalDataElements/query"),
)