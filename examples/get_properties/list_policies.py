from __future__ import annotations

import os

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


load_dotenv()


def main() -> None:
    """
    List Microsoft Purview Policies.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Policies - List")
    print("=" * 80)
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:

        policies = (
            client.policies.list_all()
        )

    print(
        f"Found {len(policies)} policies."
    )
    print()

    for index, policy in enumerate(
        policies,
        start=1,
    ):
        print("=" * 80)
        print(
            f"Policy {index}"
        )
        print("=" * 80)
        print("ID:", policy.id)
        print("Name:", policy.name)
        print(
            "Version:",
            policy.version,
        )
        print(
            "Description:",
            policy.description,
        )
        print(
            "Entity Type:",
            policy.entity_type,
        )
        print(
            "Entity Reference:",
            policy.entity_reference_name,
        )
        print()


if __name__ == "__main__":
    main()