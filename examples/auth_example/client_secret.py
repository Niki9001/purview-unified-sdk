from __future__ import annotations

import os

from azure.identity import (
    ClientSecretCredential,
)
from dotenv import load_dotenv

from purview import (
    PurviewClient,
    PurviewConfig,
)


load_dotenv()


tenant_id = os.environ[
    "PURVIEW_TENANT_ID"
]

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=os.environ[
        "PURVIEW_CLIENT_ID"
    ],
    client_secret=os.environ[
        "PURVIEW_CLIENT_SECRET"
    ],
)

config = PurviewConfig(
    tenant_id=tenant_id,
)


with PurviewClient(
    config,
    credential=credential,
) as client:
    domains = (
        client.business_domains.list_all()
    )

print(
    f"Found {len(domains)} domains."
)