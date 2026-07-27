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

# Critical Data Element:
# Fixture Name
CDE_ID = "6dcede32-65af-4390-9d38-a6e914905687"

# Glossary Term:
# test long text
GLOSSARY_TERM_ID = "35773642-3e63-4b01-ba03-f022d4f1e36c"


# =========================================================
# Relationship configuration
# =========================================================

CDE_RESOURCE_PATH = "criticalDataElements"
TERM_ENTITY_TYPE = "TERM"
RELATIONSHIP_TYPE = "Related"


# =========================================================
# Purview client configuration
# =========================================================

config = PurviewConfig(
    tenant_id=os.environ["PURVIEW_TENANT_ID"],
)


# =========================================================
# Link Glossary Term to CDE
# =========================================================

with PurviewClient(
    config,
    username=os.environ["PURVIEW_USERNAME"],
) as client:

    print("=" * 80)
    print("Critical Data Element - Add Glossary Term relationship")
    print("=" * 80)

    print("CDE ID:", CDE_ID)
    print("Glossary Term ID:", GLOSSARY_TERM_ID)
    print()

    # -----------------------------------------------------
    # Step 1: Read existing Term relationships
    # -----------------------------------------------------

    print("=" * 80)
    print("Step 1: Reading existing Glossary Term relationships")
    print("=" * 80)

    before_response = client.relationships.list_raw(
        resource_path=CDE_RESOURCE_PATH,
        resource_id=CDE_ID,
        entity_type=TERM_ENTITY_TYPE,
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
        if isinstance(item, dict)
        and item.get("entityId")
    }

    print()
    print(
        "Number of existing Glossary Term relationships:",
        len(existing_term_ids),
    )

    # -----------------------------------------------------
    # Step 2: Avoid duplicate relationship
    # -----------------------------------------------------

    if GLOSSARY_TERM_ID in existing_term_ids:
        print()
        print("=" * 80)
        print("No relationship created")
        print("=" * 80)

        print(
            "This Glossary Term is already connected "
            "to the CDE."
        )

    else:
        # -------------------------------------------------
        # Step 3: Create relationship
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Step 2: Creating Glossary Term relationship")
        print("=" * 80)

        created_relationship = client.relationships.create(
            resource_path=CDE_RESOURCE_PATH,
            resource_id=CDE_ID,
            entity_type=TERM_ENTITY_TYPE,
            entity_id=GLOSSARY_TERM_ID,
            relationship_type=RELATIONSHIP_TYPE,
            description=(
                "Glossary Term linked to CDE through "
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
            resource_path=CDE_RESOURCE_PATH,
            resource_id=CDE_ID,
            entity_type=TERM_ENTITY_TYPE,
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
            if isinstance(item, dict)
            and item.get("entityId")
        }

        print()
        print(
            "Number of Glossary Term relationships after creation:",
            len(after_term_ids),
        )

        # -------------------------------------------------
        # Step 5: Final verification
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("Final result")
        print("=" * 80)

        if GLOSSARY_TERM_ID in after_term_ids:
            print(
                "Success: the Glossary Term is now connected "
                "to the CDE."
            )
        else:
            raise RuntimeError(
                "The create request completed, but the "
                "Glossary Term was not found when the CDE "
                "relationships were read again."
            )