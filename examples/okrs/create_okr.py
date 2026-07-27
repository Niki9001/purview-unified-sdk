from __future__ import annotations

import os

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


DOMAIN_ID = os.environ[
            "PURVIEW_DOMAIN_ID"
            ]

OBJECTIVE_DEFINITION = (
    "Improve Customer Data Quality"
)

OBJECTIVE_STATUS = (
    "Draft"
)

TARGET_DATE = (
    "2027-12-31T00:00:00"
)


def main() -> None:
    """
    Create a Microsoft Purview Objective.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Objective - Create")
    print("=" * 80)
    print(
        "Definition:",
        OBJECTIVE_DEFINITION,
    )
    print(
        "Domain ID:",
        DOMAIN_ID,
    )
    print(
        "Status:",
        OBJECTIVE_STATUS,
    )
    print(
        "Target date:",
        TARGET_DATE,
    )
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:
        objective = (
            client.okrs.create_objective(
                definition=OBJECTIVE_DEFINITION,
                domain_id=DOMAIN_ID,
                status=OBJECTIVE_STATUS,
                target_date=TARGET_DATE,
            )
        )

    print("=" * 80)
    print("Created Objective")
    print("=" * 80)
    print("ID:", objective.id)
    print(
        "Definition:",
        objective.definition,
    )
    print(
        "Status:",
        objective.status,
    )
    print(
        "Domain ID:",
        objective.domain_id,
    )
    print(
        "Target date:",
        objective.target_date,
    )


if __name__ == "__main__":
    main()