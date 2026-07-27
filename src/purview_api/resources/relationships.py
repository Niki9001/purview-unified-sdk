from __future__ import annotations

from typing import Any

from purview_api.http_client import PurviewHttpClient
from purview_api.models.relationship import Relationship


class RelationshipsClient:
    """
    Client for nested Microsoft Purview relationship
    operations.

    Relationship endpoints follow this pattern:

        /{resource_path}/{resource_id}/relationships
    """

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
        Validate and normalize a required text value.
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

    def _build_path(
        self,
        resource_path: str,
        resource_id: str,
    ) -> str:
        """
        Build a nested relationship API path.
        """
        clean_resource_path = self._validate_text(
            resource_path,
            field_name="resource_path",
        ).strip("/")

        clean_resource_id = self._validate_text(
            resource_id,
            field_name="resource_id",
        )

        return (
            f"/{clean_resource_path}/"
            f"{clean_resource_id}/relationships"
        )

    def list_raw(
        self,
        resource_path: str,
        resource_id: str,
        *,
        entity_type: str | None = None,
        relationship_type: str | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        List relationships and return the complete
        API response.
        """
        request_params = dict(params or {})

        if entity_type is not None:
            request_params["entityType"] = (
                self._validate_text(
                    entity_type,
                    field_name="entity_type",
                ).upper()
            )

        if relationship_type is not None:
            request_params["relationshipType"] = (
                self._validate_text(
                    relationship_type,
                    field_name="relationship_type",
                )
            )

        response = self.http.get(
            self._build_path(
                resource_path,
                resource_id,
            ),
            params=request_params,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected relationship list "
                "response to be a dictionary."
            )

        return response

    def list(
        self,
        resource_path: str,
        resource_id: str,
        *,
        entity_type: str | None = None,
        relationship_type: str | None = None,
        params: dict[str, Any] | None = None,
    ) -> list[Relationship]:
        """
        List relationships as Relationship objects.
        """
        response = self.list_raw(
            resource_path,
            resource_id,
            entity_type=entity_type,
            relationship_type=relationship_type,
            params=params,
        )

        items = response.get("value", [])

        if not isinstance(items, list):
            raise TypeError(
                "Expected response['value'] "
                "to be a list."
            )

        return [
            Relationship.from_dict(item)
            for item in items
            if isinstance(item, dict)
        ]

    def create_raw(
        self,
        resource_path: str,
        resource_id: str,
        *,
        entity_type: str,
        payload: dict[str, Any],
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a relationship and return the raw
        API response.

        The payload is passed through unchanged
        because some Purview resources can use
        resource-specific relationship schemas.
        """
        if not isinstance(payload, dict):
            raise TypeError(
                "payload must be a dictionary."
            )

        if not payload:
            raise ValueError(
                "payload cannot be empty."
            )

        request_params = dict(params or {})
        request_params["entityType"] = (
            self._validate_text(
                entity_type,
                field_name="entity_type",
            ).upper()
        )

        response = self.http.post(
            self._build_path(
                resource_path,
                resource_id,
            ),
            params=request_params,
            json=payload,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected relationship create "
                "response to be a dictionary."
            )

        return response

    def create(
        self,
        resource_path: str,
        resource_id: str,
        *,
        entity_type: str,
        entity_id: str,
        relationship_type: str = "Related",
        description: str = "",
        params: dict[str, Any] | None = None,
    ) -> Relationship:
        """
        Create a standard relationship.

        For resource-specific payload structures,
        use create_raw().
        """
        clean_description = description

        if not isinstance(clean_description, str):
            raise TypeError(
                "description must be a string."
            )

        payload = {
            "entityId": self._validate_text(
                entity_id,
                field_name="entity_id",
            ),
            "relationshipType": (
                self._validate_text(
                    relationship_type,
                    field_name="relationship_type",
                )
            ),
            "description": clean_description,
        }

        response = self.create_raw(
            resource_path,
            resource_id,
            entity_type=entity_type,
            payload=payload,
            params=params,
        )

        return Relationship.from_dict(
            response
        )

    def delete(
        self,
        resource_path: str,
        resource_id: str,
        *,
        entity_type: str,
        entity_id: str,
        params: dict[str, Any] | None = None,
    ) -> None:
        """
        Delete a relationship.
        """
        request_params = dict(params or {})

        request_params["entityType"] = (
            self._validate_text(
                entity_type,
                field_name="entity_type",
            ).upper()
        )

        request_params["entityId"] = (
            self._validate_text(
                entity_id,
                field_name="entity_id",
            )
        )

        self.http.delete(
            self._build_path(
                resource_path,
                resource_id,
            ),
            params=request_params,
        )

    def add_objective_to_data_product(
        self,
        data_product_id: str,
        objective_id: str,
        *,
        relationship_type: str = "Related",
        description: str = "",
    ) -> Relationship:
        """
        Add an Objective relationship to a
        Data Product.
        """
        return self.create(
            resource_path="dataProducts",
            resource_id=data_product_id,
            entity_type="OBJECTIVE",
            entity_id=objective_id,
            relationship_type=relationship_type,
            description=description,
        )

    def list_data_product_objectives(
        self,
        data_product_id: str,
        *,
        relationship_type: str | None = None,
    ) -> list[Relationship]:
        """
        List Objective relationships associated
        with a Data Product.
        """
        return self.list(
            resource_path="dataProducts",
            resource_id=data_product_id,
            entity_type="OBJECTIVE",
            relationship_type=relationship_type,
        )

    def remove_objective_from_data_product(
        self,
        data_product_id: str,
        objective_id: str,
    ) -> None:
        """
        Remove an Objective relationship from a
        Data Product.
        """
        self.delete(
            resource_path="dataProducts",
            resource_id=data_product_id,
            entity_type="OBJECTIVE",
            entity_id=objective_id,
        )