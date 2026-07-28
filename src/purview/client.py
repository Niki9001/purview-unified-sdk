from __future__ import annotations

from typing import Any

from azure.core.credentials import (
    TokenCredential,
)

from purview.auth import PurviewAuthenticator
from purview.config import PurviewConfig
from purview.http_client import PurviewHttpClient

from purview.resources.business_domains import (
    BusinessDomainsClient,
)
from purview.resources.glossary_terms import (
    GlossaryTermsClient,
)
from purview.resources.cdes import (
    CriticalDataElementsClient,
)
from purview.resources.data_products import (
    DataProductsClient,
)
from purview.resources.relationships import (
    RelationshipsClient,
)
from purview.resources.data_assets import (
    DataAssetsClient,
)
from purview.navigator import PurviewNavigator
from purview.resources.okrs import OkrsClient
from purview.resources.policies import (
    PoliciesClient,
)


class PurviewClient:
    """
    Main client for interacting with Microsoft Purview APIs.

    By default, interactive browser authentication is used.

    A custom Azure TokenCredential may also be supplied.
    """

    def __init__(
        self,
        config: PurviewConfig,
        *,
        username: str | None = None,
        credential: TokenCredential | None = None,
    ) -> None:
        self.config = config

        self.authenticator = PurviewAuthenticator(
            tenant_id=config.tenant_id,
            username=username,
            credential=credential,
        )

        self.http = PurviewHttpClient(
            config=config,
            authenticator=self.authenticator,
        )

        self.business_domains = (
            BusinessDomainsClient(
                http_client=self.http,
            )
        )

        self.glossary_terms = (
            GlossaryTermsClient(
                http_client=self.http,
            )
        )

        self.cdes = CriticalDataElementsClient(
            http_client=self.http,
        )

        self.okrs = OkrsClient(
            http_client=self.http,
        )

        self.data_products = DataProductsClient(
            http_client=self.http,
        )

        self.relationships = RelationshipsClient(
            http_client=self.http,
        )

        self.data_assets = DataAssetsClient(
            http_client=self.http,
        )

        self.navigator = PurviewNavigator(
            relationships_client=(
                self.relationships
            ),
            data_assets_client=self.data_assets,
        )

        self.policies = PoliciesClient(
            http_client=self.http,
        )

    @property
    def base_url(self) -> str:
        """
        Return the Unified Catalog base URL.
        """
        return self.config.catalog_base_url

    def build_url(self, path: str) -> str:
        """
        Build a complete Purview API URL.
        """
        return self.http.build_url(path)

    def get_access_token(self) -> str:
        """
        Acquire a Purview access token.
        """
        return (
            self.authenticator.get_access_token()
        )

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send an authenticated GET request.
        """
        return self.http.get(
            path,
            params=params,
        )

    def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: (
            dict[str, Any]
            | list[Any]
            | None
        ) = None,
    ) -> Any:
        """
        Send an authenticated POST request.
        """
        return self.http.post(
            path,
            params=params,
            json=json,
        )

    def patch(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: (
            dict[str, Any]
            | list[Any]
            | None
        ) = None,
    ) -> Any:
        """
        Send an authenticated PATCH request.
        """
        return self.http.patch(
            path,
            params=params,
            json=json,
        )

    def put(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: (
            dict[str, Any]
            | list[Any]
            | None
        ) = None,
    ) -> Any:
        """
        Send an authenticated PUT request.
        """
        return self.http.put(
            path,
            params=params,
            json=json,
        )

    def delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send an authenticated DELETE request.
        """
        return self.http.delete(
            path,
            params=params,
        )

    def close(self) -> None:
        """
        Close the HTTP session and Azure credential.
        """
        self.http.close()
        self.authenticator.close()

    def __enter__(self) -> PurviewClient:
        """
        Support usage with a context manager.
        """
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        """
        Automatically close the client.
        """
        self.close()