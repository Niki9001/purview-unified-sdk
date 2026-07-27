from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class GlossaryTerm:
    """
    Represents a Microsoft Purview Glossary Term.
    """

    id: str
    name: str
    description: str | None = None
    status: str | None = None
    domain_id: str | None = None

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> GlossaryTerm:
        """
        Create a GlossaryTerm object from a Purview API response.
        """
        domain = data.get("domain")

        if isinstance(domain, dict):
            domain_id = domain.get("id")
        else:
            domain_id = domain

        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            description=data.get("description"),
            status=data.get("status"),
            domain_id=(
                str(domain_id)
                if domain_id is not None
                else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the GlossaryTerm object to a dictionary.
        """
        return asdict(self)