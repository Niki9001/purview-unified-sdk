from pprint import pprint
import os

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)

DOMAIN_ID = os.environ["PURVIEW_DOMAIN_ID"]


with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:

    term = client.glossary_terms.create(
        name="SDK Test Glossary Term",
        description="Created by the Python SDK.",
        domain_id=DOMAIN_ID,
        status="DRAFT",
    )

    print("=" * 80)
    print("Glossary Term Created")
    print("=" * 80)

    print("ID:", term.id)
    print("Name:", term.name)
    print("Description:", term.description)
    print("Status:", term.status)
    print("Domain ID:", term.domain_id)

    print()
    print("=" * 80)
    print("Raw Object")
    print("=" * 80)

    pprint(term.to_dict())