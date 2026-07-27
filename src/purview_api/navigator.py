from __future__ import annotations

from purview_api.models.data_asset import DataAsset
from purview_api.resources.data_assets import DataAssetsClient
from purview_api.resources.relationships import RelationshipsClient


class PurviewNavigator:
    """
    High-level navigation helpers for connected Purview resources.

    This class combines multiple low-level API calls into simpler
    business-oriented operations.
    """

    def __init__(
        self,
        relationships_client: RelationshipsClient,
        data_assets_client: DataAssetsClient,
    ) -> None:
        self.relationships = relationships_client
        self.data_assets = data_assets_client

    def get_data_product_assets(
        self,
        data_product_id: str,
        *,
        include_extended_properties: bool = True,
        include_lineage: bool = False,
    ) -> list[DataAsset]:
        """
        Return all Data Assets related to one Data Product.

        This method performs two steps:

        1. Find DATAASSET relationships for the Data Product.
        2. Retrieve each related Data Asset by ID.
        """
        relationships = self.relationships.list(
            resource_path="dataProducts",
            resource_id=data_product_id,
            entity_type="DATAASSET",
        )

        assets: list[DataAsset] = []

        for relationship in relationships:
            if not relationship.entity_id:
                continue

            asset = self.data_assets.get(
                relationship.entity_id,
                include_extended_properties=(
                    include_extended_properties
                ),
                include_lineage=include_lineage,
            )

            assets.append(asset)

        return assets

    def get_data_product_columns(
        self,
        data_product_id: str,
    ) -> list[dict[str, object]]:
        """
        Return columns from all Data Assets related to a Data Product.

        Each returned dictionary includes the parent asset information
        together with the column name, type, description, and
        classifications.
        """
        assets = self.get_data_product_assets(
            data_product_id,
            include_extended_properties=True,
            include_lineage=False,
        )

        columns: list[dict[str, object]] = []

        for asset in assets:
            schema = asset.raw.get("schema", [])

            if not isinstance(schema, list):
                continue

            for column in schema:
                if not isinstance(column, dict):
                    continue

                columns.append(
                    {
                        "asset_id": asset.id,
                        "asset_name": asset.name,
                        "asset_type": asset.type,
                        "column_name": column.get("name"),
                        "column_type": column.get("type"),
                        "column_description": column.get(
                            "description"
                        ),
                        "classifications": column.get(
                            "classifications",
                            [],
                        ),
                    }
                )

        return columns