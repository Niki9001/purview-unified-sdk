from __future__ import annotations

import os

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


load_dotenv()


DOMAIN_ID = (
    "315044ab-8566-4fca-a59c-5ca7c890c291"
)

OWNER_ID = os.environ[
    "PURVIEW_DATA_PRODUCT_OWNER_ID"
]

DATA_PRODUCT_NAME = (
    "SDK Test Data Product"
)

DATA_PRODUCT_DESCRIPTION = (
    "Data product created by the "
    "Purview Python SDK example."
)

DATA_PRODUCT_BUSINESS_USE = (
    "Used to test Data Product create, "
    "update, and delete operations."
)


def main() -> None:
    """
    Create a Microsoft Purview Data Product.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    contacts = {
        "owner": [
            {
                "id": OWNER_ID,
                "description": (
                    "Owner of the SDK test "
                    "Data Product."
                ),
            }
        ]
    }

    print("=" * 80)
    print("Data Product - Create")
    print("=" * 80)
    print("Domain ID:", DOMAIN_ID)
    print("Name:", DATA_PRODUCT_NAME)
    print("Type: Master")
    print("Status: DRAFT")
    print("Owner ID:", OWNER_ID)
    print(
        "Description:",
        DATA_PRODUCT_DESCRIPTION,
    )

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:
        data_product = (
            client.data_products.create(
                name=DATA_PRODUCT_NAME,
                domain_id=DOMAIN_ID,
                contacts=contacts,
                data_product_type="Master",
                status="DRAFT",
                description=(
                    DATA_PRODUCT_DESCRIPTION
                ),
                business_use=(
                    DATA_PRODUCT_BUSINESS_USE
                ),
                update_frequency="Daily",
            )
        )

        print()
        print("=" * 80)
        print(
            "Data product created successfully"
        )
        print("=" * 80)
        print("ID:", data_product.id)
        print("Name:", data_product.name)
        print(
            "Domain ID:",
            data_product.domain_id,
        )
        print("Type:", data_product.type)
        print("Status:", data_product.status)
        print(
            "Description:",
            data_product.description,
        )
        print(
            "Business use:",
            data_product.business_use,
        )
        print(
            "Update frequency:",
            data_product.update_frequency,
        )
        print(
            "Contacts:",
            data_product.contacts,
        )

        print()
        print("Created object:")
        print(data_product)


if __name__ == "__main__":
    main()