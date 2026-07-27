from __future__ import annotations

import os
from pprint import pprint

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


# =========================================================
# Load environment variables
# =========================================================

load_dotenv()


# =========================================================
# Test objects
# =========================================================

# Glossary Term:
# test long text
GLOSSARY_TERM_ID = "35773642-3e63-4b01-ba03-f022d4f1e36c"

# Replace this with a real Purview Data Column ID.
DATA_COLUMN_ID = "9d0da1c8-ff90-456d-9789-2698925eb38d"

# =========================================================
# Relationship configuration
# =========================================================

TERM_RESOURCE_PATH = "terms"
DATA_COLUMN_ENTITY_TYPE = "DATACOLUMN"
RELATIONSHIP_TYPE = "Related"


# =========================================================
# Validate test values
# =========================================================

if DATA_COLUMN_ID == "REPLACE_WITH_REAL_DATA_COLUMN_ID":
    raise ValueError(
        "Please replace DATA_COLUMN_ID with a real "
        "Purview Data Column ID."
    )


# =========================================================
# Purview client configuration
# =========================================================

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)


# =========================================================
# Link Data Column to Glossary Term
# =========================================================

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:

    print("=" * 80)
    print("Glossary Term - Add Data Column relationship")
    print("=" * 80)

    print("Glossary Term ID:", GLOSSARY_TERM_ID)
    print("Data Column ID:", DATA_COLUMN_ID)
    print("Entity type:", DATA_COLUMN_ENTITY_TYPE)
    print()

    # -----------------------------------------------------
    # Step 1: Read existing Data Column relationships
    # -----------------------------------------------------

    print("=" * 80)
    print("Step 1: Reading existing Data Column relationships")
    print("=" * 80)

    before_response = client.relationships.list_raw(
        resource_path=TERM_RESOURCE_PATH,
        resource_id=GLOSSARY_TERM_ID,
        entity_type=DATA_COLUMN_ENTITY_TYPE,
    )

    pprint(before_response, sort_dicts=False)

    before_items = before_response.get("value", [])

    if not isinstance(before_items, list):
        raise TypeError(
            "Expected response['value'] to be a list."
        )

    existing_column_ids = {
        str(item.get("entityId"))
        for item in before_items
        if isinstance(item, dict)
        and item.get("entityId")
    }

    print()
    print(
        "Number of existing Data Column relationships:",
        len(existing_column_ids),
    )

    # -----------------------------------------------------
    # Step 2: Avoid duplicate relationship
    # -----------------------------------------------------

    if DATA_COLUMN_ID in existing_column_ids:
        print()
        print("=" * 80)
        print("No relationship created")
        print("=" * 80)

        print(
            "This Data Column is already connected "
            "to the Glossary Term."
        )

    else:
        # -------------------------------------------------
        # Step 3: Create relationship
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Step 2: Creating Data Column relationship")
        print("=" * 80)

        created_relationship = client.relationships.create(
            resource_path=TERM_RESOURCE_PATH,
            resource_id=GLOSSARY_TERM_ID,
            entity_type=DATA_COLUMN_ENTITY_TYPE,
            entity_id=DATA_COLUMN_ID,
            relationship_type=RELATIONSHIP_TYPE,
            description=(
                "Data Column linked to Glossary Term through "
                "purview-api SDK test"
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
            resource_path=TERM_RESOURCE_PATH,
            resource_id=GLOSSARY_TERM_ID,
            entity_type=DATA_COLUMN_ENTITY_TYPE,
        )

        pprint(after_response, sort_dicts=False)

        after_items = after_response.get("value", [])

        if not isinstance(after_items, list):
            raise TypeError(
                "Expected response['value'] to be a list."
            )

        after_column_ids = {
            str(item.get("entityId"))
            for item in after_items
            if isinstance(item, dict)
            and item.get("entityId")
        }

        print()
        print(
            "Number of Data Column relationships after creation:",
            len(after_column_ids),
        )

        # -------------------------------------------------
        # Step 5: Final verification
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Final result")
        print("=" * 80)

        if DATA_COLUMN_ID in after_column_ids:
            print(
                "Success: the Data Column is now connected "
                "to the Glossary Term."
            )
        else:
            raise RuntimeError(
                "The create request completed, but the "
                "Data Column was not found when the Glossary "
                "Term relationships were read again."
            )