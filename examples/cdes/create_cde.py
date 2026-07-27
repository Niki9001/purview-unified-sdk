from __future__ import annotations

import os

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


load_dotenv()


DOMAIN_ID = os.environ[
            "PURVIEW_DOMAIN_ID"
            ]

CDE_NAME = (
    "SDK Test Critical Data Element"
)

CDE_DESCRIPTION = (
    "Critical Data Element created by the "
    "Purview Python SDK example."
)

CDE_DATA_TYPE = (
    "TEXT"
)

CDE_STATUS = (
    "DRAFT"
)


def main() -> None:
    """
    Create a Microsoft Purview Critical Data Element.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Critical Data Element - Create")
    print("=" * 80)
    print("Name:", CDE_NAME)
    print("Domain ID:", DOMAIN_ID)
    print("Data type:", CDE_DATA_TYPE)
    print("Status:", CDE_STATUS)
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:
        cde = client.cdes.create(
            name=CDE_NAME,
            domain_id=DOMAIN_ID,
            data_type=CDE_DATA_TYPE,
            description=CDE_DESCRIPTION,
            status=CDE_STATUS,
        )

    print("=" * 80)
    print("Created Critical Data Element")
    print("=" * 80)
    print("ID:", cde.id)
    print("Name:", cde.name)
    print("Description:", cde.description)
    print("Status:", cde.status)
    print("Data type:", cde.data_type)
    print("Domain ID:", cde.domain_id)


if __name__ == "__main__":
    main()