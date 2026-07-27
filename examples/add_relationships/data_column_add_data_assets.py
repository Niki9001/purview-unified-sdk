from __future__ import annotations

import os
from pprint import pprint

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


# =========================================================
# Test objects
# =========================================================

# Data Column:
# RUN_TYPE
DATA_COLUMN_ID = "9d0da1c8-ff90-456d-9789-2698925eb38d"

# Data Asset:
DATA_ASSET_ID = "ddc269ee-9843-4886-98f2-5afdb3aae55d"


# =========================================================
# Relationship configuration
# =========================================================

DATA_COLUMN_RESOURCE_PATH = "dataColumns"
DATA_ASSET_ENTITY_TYPE = "DATAASSET"
RELATIONSHIP_TYPE = "Related"


# =========================================================
# Purview client configuration
# =========================================================

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)


# =========================================================
# Link Data Asset to Data Column
# =========================================================

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:

    print("=" * 80)
    print("Data Column - Add Data Asset relationship")
    print("=" * 80)

    print("Data Column ID:", DATA_COLUMN_ID)
    print("Data Asset ID:", DATA_ASSET_ID)
    print()

    # -----------------------------------------------------
    # Step 1: Read existing Data Asset relationships
    # -----------------------------------------------------

    print("=" * 80)
    print("Step 1: Reading existing Data Asset relationships")
    print("=" * 80)

    before_response = client.relationships.list_raw(
        resource_path=DATA_COLUMN_RESOURCE_PATH,
        resource_id=DATA_COLUMN_ID,
        entity_type=DATA_ASSET_ENTITY_TYPE,
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
        if isinstance(item, dict)
        and item.get("entityId")
    }

    print()
    print(
        "Number of existing Data Asset relationships:",
        len(existing_asset_ids),
    )

    # -----------------------------------------------------
    # Step 2: Avoid duplicate relationship
    # -----------------------------------------------------

    if DATA_ASSET_ID in existing_asset_ids:
        print()
        print("=" * 80)
        print("No relationship created")
        print("=" * 80)

        print(
            "This Data Asset is already connected "
            "to the Data Column."
        )

    else:
        # -------------------------------------------------
        # Step 3: Create relationship
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Step 2: Creating Data Asset relationship")
        print("=" * 80)

        created_relationship = client.relationships.create(
            resource_path=DATA_COLUMN_RESOURCE_PATH,
            resource_id=DATA_COLUMN_ID,
            entity_type=DATA_ASSET_ENTITY_TYPE,
            entity_id=DATA_ASSET_ID,
            relationship_type=RELATIONSHIP_TYPE,
            description=(
                "Data Asset linked to Data Column through "
                "purview SDK SDK test"
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
            resource_path=DATA_COLUMN_RESOURCE_PATH,
            resource_id=DATA_COLUMN_ID,
            entity_type=DATA_ASSET_ENTITY_TYPE,
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
            if isinstance(item, dict)
            and item.get("entityId")
        }

        print()
        print(
            "Number of Data Asset relationships after creation:",
            len(after_asset_ids),
        )

        # -------------------------------------------------
        # Step 5: Verify from the Data Asset side
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Step 4: Verifying from Data Asset side")
        print("=" * 80)

        asset_side_response = client.relationships.list_raw(
            resource_path="dataAssets",
            resource_id=DATA_ASSET_ID,
            entity_type="DATACOLUMN",
        )

        pprint(asset_side_response, sort_dicts=False)

        asset_side_items = asset_side_response.get("value", [])

        if not isinstance(asset_side_items, list):
            raise TypeError(
                "Expected response['value'] to be a list."
            )

        asset_side_column_ids = {
            str(item.get("entityId"))
            for item in asset_side_items
            if isinstance(item, dict)
            and item.get("entityId")
        }

        # -------------------------------------------------
        # Step 6: Final result
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Final result")
        print("=" * 80)

        column_side_success = DATA_ASSET_ID in after_asset_ids
        asset_side_success = DATA_COLUMN_ID in asset_side_column_ids

        print(
            "Visible from Data Column side:",
            column_side_success,
        )

        print(
            "Visible from Data Asset side:",
            asset_side_success,
        )

        if column_side_success and asset_side_success:
            print(
                "Success: the Data Column and Data Asset "
                "are connected and visible from both sides."
            )
        elif column_side_success:
            print(
                "The relationship was created from the Data "
                "Column side, but it was not returned from "
                "the Data Asset side."
            )
        else:
            raise RuntimeError(
                "The Data Asset was not found after the "
                "relationship create request."
            )