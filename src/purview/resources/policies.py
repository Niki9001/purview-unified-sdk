from __future__ import annotations

from copy import deepcopy
from typing import Any

from purview.http_client import PurviewHttpClient
from purview.models.policy import Policy


class PoliciesClient:
    """
    Client for Microsoft Purview catalog policy
    operations.
    """

    RESOURCE_PATH = "policies"

    def __init__(
        self,
        http_client: PurviewHttpClient,
    ) -> None:
        self.http = http_client

    @staticmethod
    def _validate_text(
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Validate and normalize required text.
        """
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        clean_value = value.strip()

        if not clean_value:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        return clean_value

    def _policy_path(
        self,
        policy_id: str,
    ) -> str:
        """
        Build the path for one policy.
        """
        clean_policy_id = self._validate_text(
            policy_id,
            field_name="policy_id",
        )

        return (
            f"{self.RESOURCE_PATH}/"
            f"{clean_policy_id}"
        )

    def list_raw(
        self,
        *,
        skip_token: str | None = None,
    ) -> dict[str, Any]:
        """
        List policies and return the complete API
        response, including pagination information.
        """
        params: dict[str, Any] = {}

        if skip_token is not None:
            params["skipToken"] = (
                self._validate_text(
                    skip_token,
                    field_name="skip_token",
                )
            )

        response = self.http.get(
            self.RESOURCE_PATH,
            params=params or None,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected policy list response to "
                "be a dictionary."
            )

        return response

    def list(
        self,
        *,
        skip_token: str | None = None,
    ) -> list[Policy]:
        """
        List policies as Policy model objects.
        """
        response = self.list_raw(
            skip_token=skip_token,
        )

        items = response.get("values", [])

        if not isinstance(items, list):
            raise TypeError(
                "Expected response['values'] to "
                "be a list."
            )

        return [
            Policy.from_dict(item)
            for item in items
            if isinstance(item, dict)
        ]

    def list_all(
        self,
    ) -> list[Policy]:
        """
        Retrieve every available policy across all
        result pages.
        """
        policies: list[Policy] = []
        skip_token: str | None = None
        seen_tokens: set[str] = set()

        while True:
            response = self.list_raw(
                skip_token=skip_token,
            )

            items = response.get("values", [])

            if not isinstance(items, list):
                raise TypeError(
                    "Expected response['values'] "
                    "to be a list."
                )

            policies.extend(
                Policy.from_dict(item)
                for item in items
                if isinstance(item, dict)
            )

            next_token = response.get(
                "skipToken"
            )

            if not next_token:
                break

            if not isinstance(next_token, str):
                raise TypeError(
                    "Expected skipToken to be a "
                    "string."
                )

            if next_token in seen_tokens:
                raise RuntimeError(
                    "Policy pagination returned a "
                    "repeated skip token."
                )

            seen_tokens.add(next_token)
            skip_token = next_token

        return policies

    def update(
        self,
        policy_id: str,
        *,
        name: str,
        version: int,
        properties: dict[str, Any],
    ) -> Policy:
        """
        Update an existing Purview policy.

        The endpoint uses PUT and requires the full
        policy body.
        """
        clean_policy_id = self._validate_text(
            policy_id,
            field_name="policy_id",
        )

        clean_name = self._validate_text(
            name,
            field_name="name",
        )

        if not isinstance(version, int):
            raise TypeError(
                "version must be an integer."
            )

        if version < 0:
            raise ValueError(
                "version cannot be negative."
            )

        if not isinstance(properties, dict):
            raise TypeError(
                "properties must be a dictionary."
            )

        if not properties:
            raise ValueError(
                "properties cannot be empty."
            )

        payload: dict[str, Any] = {
            "id": clean_policy_id,
            "name": clean_name,
            "version": version,
            "properties": deepcopy(
                properties
            ),
        }

        response = self.http.put(
            self._policy_path(
                clean_policy_id
            ),
            json=payload,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected policy update response "
                "to be a dictionary."
            )

        return Policy.from_dict(response)

    def update_policy(
        self,
        policy: Policy,
    ) -> Policy:
        """
        Update a policy using an existing Policy
        model.
        """
        if not isinstance(policy, Policy):
            raise TypeError(
                "policy must be a Policy object."
            )

        return self.update(
            policy_id=policy.id,
            name=policy.name,
            version=policy.version,
            properties=policy.properties,
        )