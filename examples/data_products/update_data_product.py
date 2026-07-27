from __future__ import annotations

import os

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


# Replace this with the ID returned by the new create operation.
DATA_PRODUCT_ID = (
    "58e89aca-ef75-4d54-91da-ed0153437271"
)

NEW_DATA_PRODUCT_NAME = (
    "SDK Test Data Product Updated"
)

NEW_DESCRIPTION = (
    "Data product updated by the "
    "Purview Python SDK example."
)

NEW_BUSINESS_USE = (
    "Used to verify the Data Product "
    "update operation."
)

NEW_UPDATE_FREQUENCY = "Weekly"


def main() -> None:
    """
    Update an existing Microsoft Purview Data Product.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Data Product - Update")
    print("=" * 80)
    print("Data Product ID:", DATA_PRODUCT_ID)
    print("New name:", NEW_DATA_PRODUCT_NAME)
    print("New description:", NEW_DESCRIPTION)
    print("New business use:", NEW_BUSINESS_USE)
    print(
        "New update frequency:",
        NEW_UPDATE_FREQUENCY,
    )

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:
        data_product = (
            client.data_products.update(
                DATA_PRODUCT_ID,
                name=NEW_DATA_PRODUCT_NAME,
                description=NEW_DESCRIPTION,
                business_use=NEW_BUSINESS_USE,
                update_frequency=(
                    NEW_UPDATE_FREQUENCY
                ),
            )
        )

        print()
        print("=" * 80)
        print(
            "Data product updated successfully"
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
        print("Updated object:")
        print(data_product)


if __name__ == "__main__":
    main()