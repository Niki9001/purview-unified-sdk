from purview.config import PurviewConfig
import os

from dotenv import load_dotenv


load_dotenv()

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)



print("Tenant ID:", config.tenant_id)
print("Endpoint:", config.endpoint)
print("SDK version:", config.api_version)
print("Catalog base URL:", config.catalog_base_url)
print("Timeout:", config.request_timeout)
print("Max retries:", config.max_retries)