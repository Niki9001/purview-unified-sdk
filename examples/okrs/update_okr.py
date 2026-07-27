from __future__ import annotations

import os

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


load_dotenv()


OBJECTIVE_ID = (
    "0fa82a08-539f-4e77-9972-d687348bf5d3"
)

NEW_DEFINITION = (
    "Improve Customer Data Quality "
    "Across Enterprise Systems"
)

NEW_STATUS = (
    "Published"
)

NEW_TARGET_DATE = (
    "2028-06-30T00:00:00"
)


def main() -> None:
    """
    Update an existing Microsoft Purview Objective.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Objective - Update")
    print("=" * 80)
    print("Objective ID:", OBJECTIVE_ID)
    print("New definition:", NEW_DEFINITION)
    print("New status:", NEW_STATUS)
    print("New target date:", NEW_TARGET_DATE)
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:
        objective = (
            client.okrs.update_objective(
                objective_id=OBJECTIVE_ID,
                definition=NEW_DEFINITION,
                status=NEW_STATUS,
                target_date=NEW_TARGET_DATE,
            )
        )

    print("=" * 80)
    print("Updated Objective")
    print("=" * 80)
    print("ID:", objective.id)
    print(
        "Definition:",
        objective.definition,
    )
    print("Status:", objective.status)
    print(
        "Domain ID:",
        objective.domain_id,
    )
    print(
        "Target date:",
        objective.target_date,
    )
    print(
        "Overall status:",
        objective.overall_status,
    )
    print(
        "Key results count:",
        objective.key_results_count,
    )


if __name__ == "__main__":
    main()