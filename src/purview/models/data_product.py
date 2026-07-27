from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class DataProduct:
    """
    Represents a Microsoft Purview Data Product.
    """

    id: str
    name: str

    status: str | None = None
    type: str | None = None
    domain_id: str | None = None

    description: str | None = None
    business_use: str | None = None
    update_frequency: str | None = None

    contacts: dict[str, Any] = field(
        default_factory=dict
    )

    terms_of_use: list[Any] = field(
        default_factory=list
    )

    documentation: list[Any] = field(
        default_factory=list
    )

    managed_attributes: list[Any] = field(
        default_factory=list
    )

    audience: list[str] = field(
        default_factory=list
    )

    sensitivity_label: str | None = None
    endorsed: bool | None = None
    active_subscriber_count: int | None = None
    data_quality_score: float | None = None

    additional_properties: dict[str, Any] = field(
        default_factory=dict
    )

    system_data: dict[str, Any] = field(
        default_factory=dict
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> DataProduct:
        """
        Create a DataProduct object from a Purview API response.
        """
        domain = data.get("domain")

        if isinstance(domain, dict):
            domain_id = domain.get("id")
        else:
            domain_id = domain

        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            status=data.get("status"),
            type=data.get("type"),
            domain_id=(
                str(domain_id)
                if domain_id is not None
                else None
            ),
            description=data.get("description"),
            business_use=data.get("businessUse"),
            update_frequency=data.get(
                "updateFrequency"
            ),
            contacts=data.get("contacts") or {},
            terms_of_use=data.get(
                "termsOfUse"
            ) or [],
            documentation=data.get(
                "documentation"
            ) or [],
            managed_attributes=data.get(
                "managedAttributes"
            ) or [],
            audience=data.get("audience") or [],
            sensitivity_label=data.get(
                "sensitivityLabel"
            ),
            endorsed=data.get("endorsed"),
            active_subscriber_count=data.get(
                "activeSubscriberCount"
            ),
            data_quality_score=data.get(
                "dataQualityScore"
            ),
            additional_properties=data.get(
                "additionalProperties"
            ) or {},
            system_data=data.get(
                "systemData"
            ) or {},
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the DataProduct object to a dictionary.
        """
        return asdict(self)

    @property
    def asset_count(self) -> int | None:
        """
        Return the asset count when available.
        """
        value = self.additional_properties.get(
            "assetCount"
        )

        if value is None:
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None