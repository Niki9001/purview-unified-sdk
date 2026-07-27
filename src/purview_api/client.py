from __future__ import annotations

from typing import Any

from purview_api.auth import PurviewAuthenticator
from purview_api.config import PurviewConfig
from purview_api.http_client import PurviewHttpClient

from purview_api.resources.business_domains import BusinessDomainsClient
from purview_api.resources.glossary_terms import GlossaryTermsClient
from purview_api.resources.cdes import CriticalDataElementsClient
from purview_api.resources.data_products import DataProductsClient
from purview_api.resources.relationships import RelationshipsClient
from purview_api.resources.data_assets import DataAssetsClient
from purview_api.navigator import PurviewNavigator
from purview_api.resources.okrs import OkrsClient
from purview_api.resources.policies import (
    PoliciesClient,
)

class PurviewClient:
    """
    Main client for interacting with Microsoft Purview APIs.
    """

    def __init__(
        self,
        config: PurviewConfig,
        *,
        username: str | None = None,
    ) -> None:
        self.config = config

        self.authenticator = PurviewAuthenticator(
            tenant_id=config.tenant_id,
            username=username,
        )

        self.http = PurviewHttpClient(
            config=config,
            authenticator=self.authenticator,
        )

        self.business_domains = BusinessDomainsClient(
            http_client=self.http,
        )
        
        self.glossary_terms = GlossaryTermsClient(
            http_client=self.http,
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
            relationships_client=self.relationships,
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
        return self.authenticator.get_access_token()

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
        json: dict[str, Any] | list[Any] | None = None,
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
        json: dict[str, Any] | list[Any] | None = None,
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
        json: dict[str, Any] | list[Any] | None = None,
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
        Close the underlying HTTP session.
        """
        self.http.close()

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
        Automatically close the HTTP session.
        """
        self.close()