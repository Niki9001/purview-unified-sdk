from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PurviewConfig:
    """
    Configuration used by the Purview API client.
    """

    tenant_id: str

    endpoint: str | None = None
    api_version: str = "2026-03-20-preview"

    request_timeout: int = 60
    max_retries: int = 3

    def __post_init__(self) -> None:
        """
        Validate and normalize configuration values.
        """
        tenant_id = self.tenant_id.strip()

        if not tenant_id:
            raise ValueError("tenant_id cannot be empty.")

        if not self.api_version.strip():
            raise ValueError("api_version cannot be empty.")

        if self.request_timeout <= 0:
            raise ValueError(
                "request_timeout must be greater than 0."
            )

        if self.max_retries < 0:
            raise ValueError(
                "max_retries cannot be negative."
            )

        endpoint = self.endpoint

        if endpoint is None:
            endpoint = (
                f"https://{tenant_id}"
                "-api.purview-service.microsoft.com"
            )

        endpoint = endpoint.strip().rstrip("/")

        if not endpoint:
            raise ValueError("endpoint cannot be empty.")

        object.__setattr__(
            self,
            "tenant_id",
            tenant_id,
        )

        object.__setattr__(
            self,
            "endpoint",
            endpoint,
        )

    @property
    def catalog_base_url(self) -> str:
        """
        Base URL for Purview Unified Catalog endpoints.
        """
        return (
            f"{self.endpoint}"
            "/datagovernance/catalog"
        )