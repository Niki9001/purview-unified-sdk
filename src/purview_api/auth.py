from __future__ import annotations

from azure.core.credentials import AccessToken
from azure.identity import (
    InteractiveBrowserCredential,
    TokenCachePersistenceOptions,
)


PURVIEW_TOKEN_SCOPE = "https://purview.azure.net/.default"


class PurviewAuthenticator:
    """
    Handles Microsoft Entra interactive authentication for Purview APIs.
    """

    def __init__(
        self,
        tenant_id: str,
        *,
        username: str | None = None,
        cache_name: str = "purview_api_token_cache",
    ) -> None:
        if not tenant_id.strip():
            raise ValueError("tenant_id cannot be empty.")

        self.tenant_id = tenant_id
        self.username = username

        cache_options = TokenCachePersistenceOptions(
            name=cache_name,
            allow_unencrypted_storage=False,
        )

        self.credential = InteractiveBrowserCredential(
            tenant_id=tenant_id,
            login_hint=username,
            cache_persistence_options=cache_options,
        )

    def get_token(self) -> AccessToken:
        """
        Get a Purview access token.
        """
        return self.credential.get_token(PURVIEW_TOKEN_SCOPE)

    def get_access_token(self) -> str:
        """
        Return only the access-token string.
        """
        return self.get_token().token