from purview import PurviewClient, PurviewConfig

from pprint import pprint
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
    domains = client.business_domains.list()

    print(type(domains))
    print(type(domains[0]))

    print()
    print(domains[0].id)
    print(domains[0].name)
    print(domains[0].description)

    print()
    print(domains[0].to_dict())