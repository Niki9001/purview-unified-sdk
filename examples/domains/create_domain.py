from __future__ import annotations

import os

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


load_dotenv()


DOMAIN_NAME = os.getenv(
    "PURVIEW_NEW_DOMAIN_NAME",
    "SDK Test Business Domain",
)

DOMAIN_TYPE = os.getenv(
    "PURVIEW_NEW_DOMAIN_TYPE",
    "DataDomain",
)

DOMAIN_DESCRIPTION = os.getenv(
    "PURVIEW_NEW_DOMAIN_DESCRIPTION",
    (
        "Business domain created by the "
        "Purview Python SDK example."
    ),
)


def main() -> None:
    """
    Create a new Microsoft Purview business domain.
    """
    tenant_id = os.environ["PURVIEW_TENANT_ID"]
    username = os.environ["PURVIEW_USERNAME"]

    config = PurviewConfig(
        tenant_id=tenant_id,
    )

    print("=" * 80)
    print("Business Domain - Create")
    print("=" * 80)
    print("Domain name:", DOMAIN_NAME)
    print("Domain type:", DOMAIN_TYPE)
    print("Description:", DOMAIN_DESCRIPTION)

    with PurviewClient(
        config,
        username=username,
    ) as client:
        domain = client.business_domains.create(
            name=DOMAIN_NAME,
            domain_type=DOMAIN_TYPE,
            description=DOMAIN_DESCRIPTION,
        )

        print()
        print("=" * 80)
        print("Business domain created successfully")
        print("=" * 80)
        print("ID:", domain.id)
        print("Name:", domain.name)
        print("Description:", domain.description)
        print("Status:", domain.status)

        print()
        print("Created object:")
        print(domain)


if __name__ == "__main__":
    main()