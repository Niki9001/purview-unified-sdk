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

# Data Product:
# testing
DATA_PRODUCT_ID = "b0d4696e-0725-42bf-afeb-5b41daf56c21"

# Glossary Term:
# test long text
GLOSSARY_TERM_ID = "35773642-3e63-4b01-ba03-f022d4f1e36c"


# =========================================================
# Purview client configuration
# =========================================================

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)


# =========================================================
# Add Glossary Term to Data Product
# =========================================================

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:

    print("=" * 80)
    print("Data Product - Add Glossary Term relationship")
    print("=" * 80)

    print("Data Product ID:", DATA_PRODUCT_ID)
    print("Glossary Term ID:", GLOSSARY_TERM_ID)
    print()

    # -----------------------------------------------------
    # Step 1: Read existing Glossary Term relationships
    # -----------------------------------------------------

    print("=" * 80)
    print("Step 1: Reading existing Glossary Term relationships")
    print("=" * 80)

    before_response = client.relationships.list_raw(
        resource_path="dataProducts",
        resource_id=DATA_PRODUCT_ID,
        entity_type="TERM",
    )

    pprint(before_response, sort_dicts=False)

    before_items = before_response.get("value", [])

    if not isinstance(before_items, list):
        raise TypeError(
            "Expected response['value'] to be a list."
        )

    existing_term_ids = {
        str(item.get("entityId"))
        for item in before_items
        if isinstance(item, dict) and item.get("entityId")
    }

    print()
    print(
        "Number of existing Glossary Term relationships:",
        len(existing_term_ids),
    )

    # -----------------------------------------------------
    # Step 2: Avoid creating a duplicate relationship
    # -----------------------------------------------------

    if GLOSSARY_TERM_ID in existing_term_ids:
        print()
        print("=" * 80)
        print("No relationship created")
        print("=" * 80)

        print(
            "This Glossary Term is already connected "
            "to the Data Product."
        )

    else:
        # -------------------------------------------------
        # Step 3: Create the relationship
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Step 2: Creating Glossary Term relationship")
        print("=" * 80)

        created_relationship = client.relationships.create(
            resource_path="dataProducts",
            resource_id=DATA_PRODUCT_ID,
            entity_type="TERM",
            entity_id=GLOSSARY_TERM_ID,
            relationship_type="Related",
            description=(
                "Glossary Term added through purview-api SDK test"
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
            entity_type="TERM",
        )

        pprint(after_response, sort_dicts=False)

        after_items = after_response.get("value", [])

        if not isinstance(after_items, list):
            raise TypeError(
                "Expected response['value'] to be a list."
            )

        after_term_ids = {
            str(item.get("entityId"))
            for item in after_items
            if isinstance(item, dict) and item.get("entityId")
        }

        print()
        print(
            "Number of Glossary Term relationships after creation:",
            len(after_term_ids),
        )

        # -------------------------------------------------
        # Step 5: Final result
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Final result")
        print("=" * 80)

        if GLOSSARY_TERM_ID in after_term_ids:
            print(
                "Success: the Glossary Term is now connected "
                "to the Data Product."
            )
        else:
            raise RuntimeError(
                "The create request completed, but the Glossary Term "
                "was not found when the relationships were read again."
            )