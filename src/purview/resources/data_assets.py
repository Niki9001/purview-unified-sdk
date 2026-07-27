from __future__ import annotations

from typing import Any

from purview.models.data_asset import DataAsset
from purview.resources.base import BaseResourceClient


class DataAssetsClient(
    BaseResourceClient[DataAsset]
):
    """
    Client for Microsoft Purview Data Asset operations.
    """

    RESOURCE_PATH = "dataAssets"
    MODEL = DataAsset

    def get(
        self,
        data_asset_id: str,
        *,
        include_extended_properties: bool | None = None,
        include_lineage: bool | None = None,
        params: dict[str, Any] | None = None,
    ) -> DataAsset:
        """
        Get one Data Asset by ID.
        """
        request_params = dict(params or {})

        if include_extended_properties is not None:
            request_params["includeExtendedProperties"] = (
                include_extended_properties
            )

        if include_lineage is not None:
            request_params["includeLineage"] = (
                include_lineage
            )

        return super().get(
            data_asset_id,
            params=request_params,
        )

    def query(
        self,
        payload: dict[str, Any] | None = None,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Query Data Assets and return the raw API response.
        """
        request_payload = payload if payload is not None else {}

        response = self.http.post(
            f"{self.resource_path}/query",
            params=params,
            json=request_payload,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected Data Asset query response "
                "to be a dictionary."
            )

        return response

    def query_models(
        self,
        payload: dict[str, Any] | None = None,
        *,
        params: dict[str, Any] | None = None,
    ) -> list[DataAsset]:
        """
        Query Data Assets and return model objects.
        """
        response = self.query(
            payload=payload,
            params=params,
        )

        return self._to_model_list(response)