from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class KeyResult:
    """
    Represents a Microsoft Purview OKR Key Result.
    """

    id: str
    definition: str
    domain_id: str | None = None
    progress: float | None = None
    goal: float | None = None
    max_value: float | None = None
    status: str | None = None

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> KeyResult:
        """
        Create a KeyResult object from a Purview
        API response.
        """
        return cls(
            id=str(data.get("id", "")),
            definition=str(
                data.get("definition", "")
            ),
            domain_id=(
                str(data["domainId"])
                if data.get("domainId")
                is not None
                else None
            ),
            progress=data.get("progress"),
            goal=data.get("goal"),
            max_value=data.get("max"),
            status=data.get("status"),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the KeyResult object to a dictionary.
        """
        return asdict(self)