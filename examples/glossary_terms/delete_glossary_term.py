from __future__ import annotations

import os

from dotenv import load_dotenv

from purview import PurviewClient, PurviewConfig


load_dotenv()


GLOSSARY_TERM_ID = (
    "5da4ea04-d797-4277-9eb6-2018a1fb1c21"
)


def main() -> None:
    """
    Delete an existing Microsoft Purview Glossary Term.
    """
    config = PurviewConfig(
        tenant_id=os.environ[
            "PURVIEW_TENANT_ID"
        ],
    )

    print("=" * 80)
    print("Glossary Term - Delete")
    print("=" * 80)
    print(
        "Glossary Term ID:",
        GLOSSARY_TERM_ID,
    )
    print()

    with PurviewClient(
        config,
        username=os.environ[
            "PURVIEW_USERNAME"
        ],
    ) as client:
        client.glossary_terms.delete(
            GLOSSARY_TERM_ID
        )

    print("=" * 80)
    print("Glossary Term Deleted")
    print("=" * 80)
    print(
        "Deleted Glossary Term ID:",
        GLOSSARY_TERM_ID,
    )


if __name__ == "__main__":
    main()