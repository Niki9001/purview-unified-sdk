from __future__ import annotations

import os

from azure.identity import (
    DeviceCodeCredential,
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

config = PurviewConfig(
    tenant_id=tenant_id,
)

credential = DeviceCodeCredential(
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