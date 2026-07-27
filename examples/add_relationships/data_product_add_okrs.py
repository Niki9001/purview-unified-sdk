from __future__ import annotations

import os

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


load_dotenv()


DATA_PRODUCT_ID = (
    "a4dc1c07-354d-4e87-a192-c5c1118b0fce"
)

OBJECTIVE_ID = (
    "b74d7475-6962-4b23-8e14-93931c39017e"
)

RELATIONSHIP_TYPE = (
    "Related"
)

DESCRIPTION = (
    "Links the Data Product to its governance "
    "Objective."
)


def main() -> None:
    """
    Add an Objective relationship to a Microsoft
    Purview Data Product.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Data Product - Add Objective")
    print("=" * 80)
    print(
        "Data Product ID:",
        DATA_PRODUCT_ID,
    )
    print(
        "Objective ID:",
        OBJECTIVE_ID,
    )
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:

        relationship = (
            client.relationships
            .add_objective_to_data_product(
                data_product_id=DATA_PRODUCT_ID,
                objective_id=OBJECTIVE_ID,
                relationship_type=RELATIONSHIP_TYPE,
                description=DESCRIPTION,
            )
        )

    print("=" * 80)
    print("Objective Relationship Added")
    print("=" * 80)

    print(
        "Entity ID:",
        relationship.entity_id,
    )
    print(
        "Relationship Type:",
        relationship.relationship_type,
    )
    print(
        "Description:",
        relationship.description,
    )


if __name__ == "__main__":
    main()