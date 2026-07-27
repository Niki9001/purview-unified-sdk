from purview_api import PurviewClient, PurviewConfig
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

token = client.get_access_token()

print("Authentication successful:", bool(token))
print("Token length:", len(token))
print("Token preview:", token[:20] + "...")