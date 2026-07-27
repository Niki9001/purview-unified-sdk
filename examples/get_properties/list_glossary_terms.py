from purview import PurviewClient, PurviewConfig
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
    terms = client.glossary_terms.list()

    print(type(terms))
    print(type(terms[0]))

    print()
    print(terms[0].id)
    print(terms[0].name)
    print(terms[0].description)
    print(terms[0].status)
    print(terms[0].domain_id)

    print()
    print(terms[0].to_dict())