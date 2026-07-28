from __future__ import annotations

from typing import Any

from azure.core.credentials import (
    AccessToken,
    TokenCredential,
)
from azure.identity import (
    InteractiveBrowserCredential,
    TokenCachePersistenceOptions,
)


PURVIEW_TOKEN_SCOPE = (
    "https://purview.azure.net/.default"
)


class PurviewAuthenticator:
    """
    Handles Microsoft Entra authentication for Purview APIs.

    By default, InteractiveBrowserCredential is used.

    A custom Azure TokenCredential can also be supplied, including:

    - DeviceCodeCredential
    - ClientSecretCredential
    - ManagedIdentityCredential
    - DefaultAzureCredential
    - AzureCliCredential
    """

    def __init__(
        self,
        tenant_id: str,
        *,
        username: str | None = None,
        credential: TokenCredential | None = None,
        cache_name: str = "purview_token_cache",
    ) -> None:
        tenant_id = tenant_id.strip()

        if not tenant_id:
            raise ValueError(
                "tenant_id cannot be empty."
            )

        self.tenant_id = tenant_id
        self.username = username

        if credential is not None:
            self.credential = credential
            return

        cache_options = (
            TokenCachePersistenceOptions(
                name=cache_name,
                allow_unencrypted_storage=False,
            )
        )

        self.credential = (
            InteractiveBrowserCredential(
                tenant_id=tenant_id,
                login_hint=username,
                cache_persistence_options=(
                    cache_options
                ),
            )
        )

    def get_token(self) -> AccessToken:
        """
        Get a Purview access token.
        """
        return self.credential.get_token(
            PURVIEW_TOKEN_SCOPE
        )

    def get_access_token(self) -> str:
        """
        Return only the access-token string.
        """
        return self.get_token().token

    def close(self) -> None:
        """
        Close the underlying Azure credential if supported.
        """
        close_method: Any = getattr(
            self.credential,
            "close",
            None,
        )

        if callable(close_method):
            close_method()