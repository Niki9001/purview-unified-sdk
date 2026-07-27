from __future__ import annotations

import os
from pprint import pprint

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


# =========================================================
# Load environment variables
# =========================================================

load_dotenv()


# =========================================================
# Test objects
# =========================================================

# Data Product:
# testing
DATA_PRODUCT_ID = "b0d4696e-0725-42bf-afeb-5b41daf56c21"

# Replace this with the Data Asset that you want to add.
DATA_ASSET_ID = "ddc269ee-9843-4886-98f2-5afdb3aae55d"


# =========================================================
# Validate local configuration
# =========================================================

if DATA_ASSET_ID == "REPLACE_WITH_REAL_DATA_ASSET_ID":
    raise ValueError(
        "Please replace DATA_ASSET_ID with a real Purview Data Asset ID."
    )


# =========================================================
# Purview client configuration
# =========================================================

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)


# =========================================================
# Add Data Asset to Data Product
# =========================================================

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:

    print("=" * 80)
    print("Data Product - Add Data Asset relationship")
    print("=" * 80)

    print("Data Product ID:", DATA_PRODUCT_ID)
    print("Data Asset ID:", DATA_ASSET_ID)
    print()

    # -----------------------------------------------------
    # Step 1: Read existing Data Asset relationships
    # -----------------------------------------------------

    print("=" * 80)
    print("Step 1: Reading existing Data Asset relationships")
    print("=" * 80)

    before_response = client.relationships.list_raw(
        resource_path="dataProducts",
        resource_id=DATA_PRODUCT_ID,
        entity_type="DATAASSET",
    )

    pprint(before_response, sort_dicts=False)

    before_items = before_response.get("value", [])

    if not isinstance(before_items, list):
        raise TypeError(
            "Expected response['value'] to be a list."
        )

    existing_asset_ids = {
        str(item.get("entityId"))
        for item in before_items
        if isinstance(item, dict) and item.get("entityId")
    }

    print()
    print(
        "Number of existing Data Asset relationships:",
        len(existing_asset_ids),
    )

    # -----------------------------------------------------
    # Step 2: Avoid creating a duplicate relationship
    # -----------------------------------------------------

    if DATA_ASSET_ID in existing_asset_ids:
        print()
        print("=" * 80)
        print("No relationship created")
        print("=" * 80)

        print(
            "This Data Asset is already connected "
            "to the Data Product."
        )

    else:
        # -------------------------------------------------
        # Step 3: Create the relationship
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Step 2: Creating Data Asset relationship")
        print("=" * 80)

        created_relationship = client.relationships.create(
            resource_path="dataProducts",
            resource_id=DATA_PRODUCT_ID,
            entity_type="DATAASSET",
            entity_id=DATA_ASSET_ID,
            relationship_type="Related",
            description=(
                "Data Asset added through purview SDK SDK test"
            ),
        )

        print("Relationship creation response:")
        pprint(
            created_relationship.to_dict(),
            sort_dicts=False,
        )

        # -------------------------------------------------
        # Step 4: Read relationships again
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Step 3: Verifying the new relationship")
        print("=" * 80)

        after_response = client.relationships.list_raw(
            resource_path="dataProducts",
            resource_id=DATA_PRODUCT_ID,
            entity_type="DATAASSET",
        )

        pprint(after_response, sort_dicts=False)

        after_items = after_response.get("value", [])

        if not isinstance(after_items, list):
            raise TypeError(
                "Expected response['value'] to be a list."
            )

        after_asset_ids = {
            str(item.get("entityId"))
            for item in after_items
            if isinstance(item, dict) and item.get("entityId")
        }

        print()
        print(
            "Number of Data Asset relationships after creation:",
            len(after_asset_ids),
        )

        # -------------------------------------------------
        # Step 5: Final result
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Final result")
        print("=" * 80)

        if DATA_ASSET_ID in after_asset_ids:
            print(
                "Success: the Data Asset is now connected "
                "to the Data Product."
            )
        else:
            raise RuntimeError(
                "The create request completed, but the Data Asset "
                "was not found when the relationships were read again."
            )