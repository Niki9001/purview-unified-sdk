from __future__ import annotations

import os

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


DOMAIN_ID = (
    "f8ae8834-8f07-46cb-8ef3-b1cd67875233"
)

NEW_DOMAIN_NAME = (
    "SDK Test Business Domain Updated"
)

NEW_DOMAIN_DESCRIPTION = (
    "Business domain updated by the "
    "Purview Python SDK example."
)


def main() -> None:
    """
    Update an existing Microsoft Purview business domain.
    """
    tenant_id = os.environ[
        "PURVIEW_TENANT_ID"
    ]

    username = os.environ[
        "PURVIEW_USERNAME"
    ]

    config = PurviewConfig(
        tenant_id=tenant_id,
    )

    print("=" * 80)
    print("Business Domain - Update")
    print("=" * 80)
    print("Domain ID:", DOMAIN_ID)
    print("New name:", NEW_DOMAIN_NAME)
    print(
        "New description:",
        NEW_DOMAIN_DESCRIPTION,
    )

    with PurviewClient(
        config,
        username=username,
    ) as client:
        domain = client.business_domains.update(
            DOMAIN_ID,
            name=NEW_DOMAIN_NAME,
            description=NEW_DOMAIN_DESCRIPTION,
        )

        print()
        print("=" * 80)
        print(
            "Business domain updated successfully"
        )
        print("=" * 80)
        print("ID:", domain.id)
        print("Name:", domain.name)
        print(
            "Description:",
            domain.description,
        )
        print("Status:", domain.status)

        print()
        print("Updated object:")
        print(domain)


if __name__ == "__main__":
    main()