from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Relationship:
    """
    Represents a Microsoft Purview relationship.
    """

    entity_id: str
    relationship_type: str | None = None
    description: str | None = None
    system_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> Relationship:
        """
        Create a Relationship object from a Purview API response.
        """
        return cls(
            entity_id=str(data.get("entityId", "")),
            relationship_type=data.get("relationshipType"),
            description=data.get("description"),
            system_data=data.get("systemData") or {},
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the Relationship object to a dictionary.
        """
        return asdict(self)