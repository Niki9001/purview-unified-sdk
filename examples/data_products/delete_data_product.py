from __future__ import annotations

import os

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


DATA_PRODUCT_ID = (
    "58e89aca-ef75-4d54-91da-ed0153437271"
)


def main() -> None:
    """
    Delete an existing Microsoft Purview Data Product.
    """
    config = PurviewConfig(
        tenant_id=os.environ["PURVIEW_TENANT_ID"],
    )

    print("=" * 80)
    print("Data Product - Delete")
    print("=" * 80)
    print("Data Product ID:", DATA_PRODUCT_ID)

    confirmation = input(
        "Type DELETE to confirm deletion: "
    ).strip()

    if confirmation != "DELETE":
        print("Deletion cancelled.")
        return

    with PurviewClient(
        config,
        username=os.environ["PURVIEW_USERNAME"],
    ) as client:
        client.data_products.delete(
            DATA_PRODUCT_ID,
        )

        print()
        print("=" * 80)
        print("Data Product deleted successfully")
        print("=" * 80)
        print("Deleted Data Product ID:", DATA_PRODUCT_ID)


if __name__ == "__main__":
    main()