from __future__ import annotations

import os

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


CDE_ID = (
    "610a953f-6d36-487c-9402-ecd324d33a69"
)

NEW_CDE_NAME = (
    "SDK Test Critical Data Element Updated"
)

NEW_DESCRIPTION = (
    "Critical Data Element updated by the "
    "Purview Python SDK example."
)

NEW_DATA_TYPE = (
    "TEXT"
)

NEW_STATUS = (
    "DRAFT"
)


def main() -> None:
    """
    Update an existing Microsoft Purview
    Critical Data Element.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Critical Data Element - Update")
    print("=" * 80)
    print("CDE ID:", CDE_ID)
    print("New name:", NEW_CDE_NAME)
    print("New description:", NEW_DESCRIPTION)
    print("New data type:", NEW_DATA_TYPE)
    print("New status:", NEW_STATUS)
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:
        cde = client.cdes.update(
            cde_id=CDE_ID,
            name=NEW_CDE_NAME,
            description=NEW_DESCRIPTION,
            data_type=NEW_DATA_TYPE,
            status=NEW_STATUS,
        )

    print("=" * 80)
    print("Updated Critical Data Element")
    print("=" * 80)
    print("ID:", cde.id)
    print("Name:", cde.name)
    print("Description:", cde.description)
    print("Status:", cde.status)
    print("Data type:", cde.data_type)
    print("Domain ID:", cde.domain_id)


if __name__ == "__main__":
    main()