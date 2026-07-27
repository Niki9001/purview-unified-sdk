from __future__ import annotations

import os

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


CDE_ID = (
    "610a953f-6d36-487c-9402-ecd324d33a69"
)


def main() -> None:
    """
    Delete an existing Microsoft Purview
    Critical Data Element.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Critical Data Element - Delete")
    print("=" * 80)
    print("CDE ID:", CDE_ID)
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:
        client.cdes.delete(
            CDE_ID
        )

    print("=" * 80)
    print("Critical Data Element Deleted")
    print("=" * 80)
    print("Deleted CDE ID:", CDE_ID)


if __name__ == "__main__":
    main()