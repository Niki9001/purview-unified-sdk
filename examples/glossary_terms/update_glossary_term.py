from __future__ import annotations

import os

from dotenv import load_dotenv

from purview_api import PurviewClient, PurviewConfig


load_dotenv()


GLOSSARY_TERM_ID = (
    "5da4ea04-d797-4277-9eb6-2018a1fb1c21"
)

NEW_NAME = (
    "SDK Test Glossary Term Updated"
)

NEW_DESCRIPTION = (
    "Glossary term updated by the "
    "Purview Python SDK example."
)


def main() -> None:
    """
    Update an existing Microsoft Purview Glossary Term.
    """

    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Glossary Term - Update")
    print("=" * 80)
    print("Glossary Term ID:", GLOSSARY_TERM_ID)
    print("New name:", NEW_NAME)
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:

        glossary_term = (
            client.glossary_terms.update(
                term_id=GLOSSARY_TERM_ID,
                name=NEW_NAME,
                description=NEW_DESCRIPTION,
            )
        )

    print("=" * 80)
    print("Updated Glossary Term")
    print("=" * 80)
    print("ID:", glossary_term.id)
    print("Name:", glossary_term.name)
    print(
        "Description:",
        glossary_term.description,
    )
    print("Status:", glossary_term.status)
    print(
        "Domain ID:",
        glossary_term.domain_id,
    )


if __name__ == "__main__":
    main()