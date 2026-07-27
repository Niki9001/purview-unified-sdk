from __future__ import annotations

import os

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


load_dotenv()


OBJECTIVE_ID = (
    "0fa82a08-539f-4e77-9972-d687348bf5d3"
)


def main() -> None:
    """
    Delete an existing Microsoft Purview Objective.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Objective - Delete")
    print("=" * 80)
    print("Objective ID:", OBJECTIVE_ID)
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:
        client.okrs.delete_objective(
            OBJECTIVE_ID
        )

    print("=" * 80)
    print("Objective Deleted")
    print("=" * 80)
    print(
        "Deleted Objective ID:",
        OBJECTIVE_ID,
    )


if __name__ == "__main__":
    main()