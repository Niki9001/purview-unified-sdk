from __future__ import annotations

import os
from pprint import pprint

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


# =========================================================
# Test objects
# =========================================================

DATA_PRODUCT_ID = "b0d4696e-0725-42bf-afeb-5b41daf56c21"
DATA_ASSET_ID = "ddc269ee-9843-4886-98f2-5afdb3aae55d"


# =========================================================
# Relationship configuration
# =========================================================

DATA_ASSET_RESOURCE_PATH = "dataAssets"
DATA_PRODUCT_ENTITY_TYPE = "DATAPRODUCT"
RELATIONSHIP_TYPE = "Related"


# =========================================================
# Purview client configuration
# =========================================================

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)


with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:

    print("=" * 80)
    print("Data Asset - Add Data Product relationship")
    print("=" * 80)

    print("Data Asset ID:", DATA_ASSET_ID)
    print("Data Product ID:", DATA_PRODUCT_ID)
    print()

    # -----------------------------------------------------
    # Step 1: Read existing Data Product relationships
    # from the Data Asset side
    # -----------------------------------------------------

    print("=" * 80)
    print("Step 1: Reading existing Data Product relationships")
    print("=" * 80)

    before_response = client.relationships.list_raw(
        resource_path=DATA_ASSET_RESOURCE_PATH,
        resource_id=DATA_ASSET_ID,
        entity_type=DATA_PRODUCT_ENTITY_TYPE,
    )

    pprint(before_response, sort_dicts=False)

    before_items = before_response.get("value", [])

    if not isinstance(before_items, list):
        raise TypeError(
            "Expected response['value'] to be a list."
        )

    existing_product_ids = {
        str(item.get("entityId"))
        for item in before_items
        if isinstance(item, dict)
        and item.get("entityId")
    }

    print()
    print(
        "Number of existing Data Product relationships:",
        len(existing_product_ids),
    )

    already_exists = DATA_PRODUCT_ID in existing_product_ids

    print(
        "Target relationship already exists:",
        already_exists,
    )

    # -----------------------------------------------------
    # Step 2: Attempt to create from the reverse side
    # -----------------------------------------------------

    print()
    print("=" * 80)
    print("Step 2: Creating relationship from Data Asset side")
    print("=" * 80)

    try:
        created_relationship = client.relationships.create(
            resource_path=DATA_ASSET_RESOURCE_PATH,
            resource_id=DATA_ASSET_ID,
            entity_type=DATA_PRODUCT_ENTITY_TYPE,
            entity_id=DATA_PRODUCT_ID,
            relationship_type=RELATIONSHIP_TYPE,
            description=(
                "Reverse-side relationship test through "
                "purview SDK SDK"
            ),
        )

        print("Create request returned successfully:")

        pprint(
            created_relationship.to_dict(),
            sort_dicts=False,
        )

    except RuntimeError as exc:
        print("Create request returned an API error:")
        print(exc)

    # -----------------------------------------------------
    # Step 3: Read again from the Data Asset side
    # -----------------------------------------------------

    print()
    print("=" * 80)
    print("Step 3: Reading relationships after create attempt")
    print("=" * 80)

    after_response = client.relationships.list_raw(
        resource_path=DATA_ASSET_RESOURCE_PATH,
        resource_id=DATA_ASSET_ID,
        entity_type=DATA_PRODUCT_ENTITY_TYPE,
    )

    pprint(after_response, sort_dicts=False)

    after_items = after_response.get("value", [])

    if not isinstance(after_items, list):
        raise TypeError(
            "Expected response['value'] to be a list."
        )

    after_product_ids = [
        str(item.get("entityId"))
        for item in after_items
        if isinstance(item, dict)
        and item.get("entityId")
    ]

    matching_count = sum(
        product_id == DATA_PRODUCT_ID
        for product_id in after_product_ids
    )

    print()
    print(
        "Number of matching relationships after create attempt:",
        matching_count,
    )

    # -----------------------------------------------------
    # Step 4: Verify from the Data Product side
    # -----------------------------------------------------

    print()
    print("=" * 80)
    print("Step 4: Verifying from Data Product side")
    print("=" * 80)

    product_side_response = client.relationships.list_raw(
        resource_path="dataProducts",
        resource_id=DATA_PRODUCT_ID,
        entity_type="DATAASSET",
    )

    pprint(product_side_response, sort_dicts=False)

    product_side_items = product_side_response.get("value", [])

    if not isinstance(product_side_items, list):
        raise TypeError(
            "Expected response['value'] to be a list."
        )

    product_side_matches = sum(
        str(item.get("entityId")) == DATA_ASSET_ID
        for item in product_side_items
        if isinstance(item, dict)
    )

    # -----------------------------------------------------
    # Step 5: Final result
    # -----------------------------------------------------

    print()
    print("=" * 80)
    print("Final result")
    print("=" * 80)

    print(
        "Matches from Data Asset side:",
        matching_count,
    )

    print(
        "Matches from Data Product side:",
        product_side_matches,
    )

    if matching_count == 1 and product_side_matches == 1:
        print(
            "Result: both endpoints refer to the same single "
            "Data Product-Data Asset relationship."
        )
    elif matching_count > 1 or product_side_matches > 1:
        print(
            "Warning: duplicate relationships appear to exist."
        )
    else:
        print(
            "Result is inconclusive. Review the API response above."
        )