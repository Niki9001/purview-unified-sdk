from __future__ import annotations

from typing import Any

import requests

from purview_api.auth import PurviewAuthenticator
from purview_api.config import PurviewConfig


class PurviewHttpClient:
    """
    Low-level HTTP client for Microsoft Purview APIs.
    """

    def __init__(
        self,
        config: PurviewConfig,
        authenticator: PurviewAuthenticator,
    ) -> None:
        self.config = config
        self.authenticator = authenticator
        self.session = requests.Session()

    def build_url(self, path: str) -> str:
        """
        Build a complete Purview Unified Catalog API URL.
        """
        clean_path = path.strip()

        if not clean_path:
            raise ValueError("path cannot be empty.")

        return (
            f"{self.config.catalog_base_url}/"
            f"{clean_path.lstrip('/')}"
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | list[Any] | None = None,
    ) -> Any:
        """
        Send an authenticated HTTP request to Purview.
        """
        url = self.build_url(path)
        token = self.authenticator.get_access_token()

        request_params = dict(params or {})
        request_params.setdefault(
            "api-version",
            self.config.api_version,
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        response = self.session.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=request_params,
            json=json,
            timeout=self.config.request_timeout,
        )

        if not response.ok:
            try:
                error_detail = response.json()
            except ValueError:
                error_detail = response.text

            raise RuntimeError(
                "\nPurview API request failed.\n"
                f"Method: {method.upper()}\n"
                f"URL: {response.url}\n"
                f"Status: {response.status_code}\n"
                f"Reason: {response.reason}\n"
                f"x-ms-error-code: "
                f"{response.headers.get('x-ms-error-code')}\n"
                f"x-ms-request-id: "
                f"{response.headers.get('x-ms-request-id')}\n"
                f"Response: {error_detail}"
            )

        if response.status_code == 204:
            return None

        if not response.content:
            return None

        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError(
                "\nPurview API returned a non-JSON response.\n"
                f"Method: {method.upper()}\n"
                f"URL: {response.url}\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            ) from exc

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self.request(
            "GET",
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
        return self.request(
            "POST",
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
        return self.request(
            "PATCH",
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
        return self.request(
            "PUT",
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
        return self.request(
            "DELETE",
            path,
            params=params,
        )

    def close(self) -> None:
        """
        Close the underlying HTTP session.
        """
        self.session.close()