from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class BusinessDomain:
    """
    Represents a Microsoft Purview Business Domain.
    """

    id: str
    name: str
    description: str | None = None
    status: str | None = None

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> BusinessDomain:
        """
        Create a BusinessDomain object from a Purview API response.
        """
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            description=data.get("description"),
            status=data.get("status"),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the BusinessDomain object to a dictionary.
        """
        return asdict(self)