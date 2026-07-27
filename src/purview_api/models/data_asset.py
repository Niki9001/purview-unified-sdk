from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class DataAsset:
    """
    Represents a Microsoft Purview Data Asset.
    """

    id: str
    name: str

    type: str | None = None
    description: str | None = None
    domain_id: str | None = None
    open_in_url: str | None = None

    source: dict[str, Any] = field(default_factory=dict)
    contacts: dict[str, Any] = field(default_factory=dict)
    classifications: list[dict[str, Any]] = field(
        default_factory=list
    )
    extended_properties: dict[str, Any] = field(
        default_factory=dict
    )
    additional_properties: dict[str, Any] = field(
        default_factory=dict
    )
    system_data: dict[str, Any] = field(
        default_factory=dict
    )
    type_properties: dict[str, Any] = field(
        default_factory=dict
    )

    is_migrated: bool | None = None
    lineage: dict[str, Any] | list[Any] | None = None

    raw: dict[str, Any] = field(
        default_factory=dict,
        repr=False,
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> DataAsset:
        """
        Create a DataAsset object from a Purview API response.
        """
        if not isinstance(data, dict):
            raise TypeError(
                "data must be a dictionary."
            )

        domain = data.get("domain")

        if isinstance(domain, dict):
            domain_id = domain.get("id")
        else:
            domain_id = domain

        classifications = data.get("classifications")

        if not isinstance(classifications, list):
            classifications = []

        return cls(
            id=str(
                data.get("id")
                or data.get("dataAssetId")
                or ""
            ),
            name=str(
                data.get("name")
                or data.get("displayName")
                or ""
            ),
            type=data.get("type"),
            description=data.get("description"),
            domain_id=(
                str(domain_id)
                if domain_id is not None
                else None
            ),
            open_in_url=(
                data.get("openInUrl")
                or data.get("openInURL")
            ),
            source=data.get("source") or {},
            contacts=data.get("contacts") or {},
            classifications=[
                item
                for item in classifications
                if isinstance(item, dict)
            ],
            extended_properties=(
                data.get("extendedProperties") or {}
            ),
            additional_properties=(
                data.get("additionalProperties") or {}
            ),
            system_data=data.get("systemData") or {},
            type_properties=data.get("typeProperties") or {},
            is_migrated=data.get("isMigrated"),
            lineage=data.get("lineage"),
            raw=dict(data),
        )

    @property
    def source_type(self) -> str | None:
        """
        Return the source asset type.

        Example:
        sap_s4hana_table
        snowflake_table
        """
        value = self.source.get("assetType")

        if value is None:
            return None

        return str(value)

    @property
    def source_system_type(self) -> str | None:
        """
        Return the source system category.

        Example:
        PurviewDataMap
        """
        value = self.source.get("type")

        if value is None:
            return None

        return str(value)

    @property
    def account_name(self) -> str | None:
        """
        Return the Purview source account name.
        """
        value = self.source.get("accountName")

        if value is None:
            return None

        return str(value)

    @property
    def source_asset_id(self) -> str | None:
        """
        Return the underlying Data Map asset ID.
        """
        value = self.source.get("assetId")

        if value is None:
            return None

        return str(value)

    @property
    def fqn(self) -> str | None:
        """
        Return the fully qualified name of the asset.
        """
        value = self.source.get("fqn")

        if value is None:
            return None

        return str(value)

    @property
    def qualified_name(self) -> str | None:
        """
        Return the qualified name from source asset attributes.
        """
        value = self.asset_attributes.get(
            "qualifiedName"
        )

        if value is None:
            return self.fqn

        return str(value)

    @property
    def asset_attributes(self) -> dict[str, Any]:
        """
        Return source asset attributes.
        """
        value = self.source.get("assetAttributes", {})

        if not isinstance(value, dict):
            return {}

        return value

    @property
    def columns(self) -> list[dict[str, Any]]:
        """
        Return asset schema columns.
        """
        schema = self.raw.get("schema", [])

        if not isinstance(schema, list):
            return []

        return [
            item
            for item in schema
            if isinstance(item, dict)
        ]

    @property
    def column_count(self) -> int:
        """
        Return the number of schema columns.
        """
        return len(self.columns)

    @property
    def created_at(self) -> str | None:
        """
        Return the asset creation timestamp.
        """
        value = self.system_data.get("createdAt")

        if value is None:
            return None

        return str(value)

    @property
    def last_modified_at(self) -> str | None:
        """
        Return the last modified timestamp.
        """
        value = self.system_data.get(
            "lastModifiedAt"
        )

        if value is None:
            return None

        return str(value)

    @property
    def provisioning_state(self) -> str | None:
        """
        Return the provisioning state.
        """
        value = self.system_data.get(
            "provisioningState"
        )

        if value is None:
            return None

        return str(value)

    def get_column(
        self,
        column_name: str,
        *,
        case_sensitive: bool = False,
    ) -> dict[str, Any] | None:
        """
        Find one schema column by name.
        """
        if not isinstance(column_name, str):
            raise TypeError(
                "column_name must be a string."
            )

        clean_name = column_name.strip()

        if not clean_name:
            raise ValueError(
                "column_name cannot be empty."
            )

        for column in self.columns:
            name = column.get("name")

            if not isinstance(name, str):
                continue

            if case_sensitive:
                if name == clean_name:
                    return column
            else:
                if name.casefold() == clean_name.casefold():
                    return column

        return None

    def to_dict(
        self,
        *,
        include_raw: bool = False,
    ) -> dict[str, Any]:
        """
        Convert the DataAsset object to a dictionary.

        Parameters
        ----------
        include_raw:
            Include the complete original API response.
        """
        result = asdict(self)

        if not include_raw:
            result.pop("raw", None)

        result["source_type"] = self.source_type
        result["source_system_type"] = (
            self.source_system_type
        )
        result["account_name"] = self.account_name
        result["source_asset_id"] = (
            self.source_asset_id
        )
        result["fqn"] = self.fqn
        result["qualified_name"] = (
            self.qualified_name
        )
        result["column_count"] = self.column_count
        result["created_at"] = self.created_at
        result["last_modified_at"] = (
            self.last_modified_at
        )
        result["provisioning_state"] = (
            self.provisioning_state
        )

        return result