from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Policy:
    """
    Represents a Microsoft Purview catalog policy.
    """

    id: str
    name: str
    version: int
    properties: dict[str, Any] = field(
        default_factory=dict
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> Policy:
        """
        Create a Policy object from a Purview API
        response.
        """
        properties = data.get("properties")

        if not isinstance(properties, dict):
            properties = {}

        version = data.get("version", 0)

        if not isinstance(version, int):
            try:
                version = int(version)
            except (TypeError, ValueError):
                version = 0

        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            version=version,
            properties=properties,
        )

    @property
    def description(self) -> str | None:
        """
        Return the policy description.
        """
        value = self.properties.get(
            "description"
        )

        return (
            str(value)
            if value is not None
            else None
        )

    @property
    def entity_type(self) -> str | None:
        """
        Return the policy entity reference type.
        """
        entity = self.properties.get("entity")

        if not isinstance(entity, dict):
            return None

        value = entity.get("type")

        return (
            str(value)
            if value is not None
            else None
        )

    @property
    def entity_reference_name(
        self,
    ) -> str | None:
        """
        Return the referenced Purview entity ID.
        """
        entity = self.properties.get("entity")

        if not isinstance(entity, dict):
            return None

        value = entity.get("referenceName")

        return (
            str(value)
            if value is not None
            else None
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the Policy object to a dictionary.
        """
        return asdict(self)

    def to_api_dict(self) -> dict[str, Any]:
        """
        Convert the Policy into an API request body.
        """
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "properties": self.properties,
        }