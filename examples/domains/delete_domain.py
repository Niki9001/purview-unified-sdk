from __future__ import annotations

import os

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


load_dotenv()


DOMAIN_ID = "c51be2b8-9db4-462a-ad1c-1bc29d1f735a"


def main() -> None:
    """
    Delete an existing Microsoft Purview business domain.
    """
    tenant_id = os.environ["PURVIEW_TENANT_ID"]
    username = os.environ["PURVIEW_USERNAME"]

    config = PurviewConfig(
        tenant_id=tenant_id,
    )

    print("=" * 80)
    print("Business Domain - Delete")
    print("=" * 80)
    print("Domain ID:", DOMAIN_ID)

    confirmation = input(
        "Type DELETE to confirm deletion: "
    ).strip()

    if confirmation != "DELETE":
        print("Deletion cancelled.")
        return

    with PurviewClient(
        config,
        username=username,
    ) as client:
        client.business_domains.delete(
            DOMAIN_ID
        )

        print()
        print("=" * 80)
        print("Business domain deleted successfully")
        print("=" * 80)
        print("Deleted domain ID:", DOMAIN_ID)


if __name__ == "__main__":
    main()