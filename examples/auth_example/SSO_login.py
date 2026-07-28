from __future__ import annotations

import os

from dotenv import load_dotenv

from purview import (
    PurviewClient,
    PurviewConfig,
)


load_dotenv()


config = PurviewConfig(
    tenant_id=os.environ[
        "PURVIEW_TENANT_ID"
    ],
)


with PurviewClient(
    config,
    username=os.environ[
        "PURVIEW_USERNAME"
    ],
) as client:
    domains = (
        client.business_domains.list_all()
    )

print(
    f"Found {len(domains)} domains."
)