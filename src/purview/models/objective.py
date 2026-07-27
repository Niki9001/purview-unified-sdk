from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Objective:
    """
    Represents a Microsoft Purview Objective (OKR).
    """

    id: str
    definition: str
    status: str | None = None
    domain_id: str | None = None
    target_date: str | None = None

    overall_progress: float | None = None
    overall_goal: float | None = None
    overall_max: float | None = None
    overall_status: str | None = None
    key_results_count: int | None = None

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> Objective:
        """
        Create an Objective object from a Purview
        API response.
        """
        domain = data.get("domain")

        if isinstance(domain, dict):
            domain_id = domain.get("id")
        else:
            domain_id = domain

        additional_properties = data.get(
            "additionalProperties"
        )

        if not isinstance(
            additional_properties,
            dict,
        ):
            additional_properties = {}

        return cls(
            id=str(data.get("id", "")),
            definition=str(
                data.get("definition", "")
            ),
            status=data.get("status"),
            domain_id=(
                str(domain_id)
                if domain_id is not None
                else None
            ),
            target_date=(
                data.get("targetDate")
                or data.get("target_date")
            ),
            overall_progress=(
                additional_properties.get(
                    "overallProgress"
                )
            ),
            overall_goal=(
                additional_properties.get(
                    "overallGoal"
                )
            ),
            overall_max=(
                additional_properties.get(
                    "overallMax"
                )
            ),
            overall_status=(
                additional_properties.get(
                    "overallStatus"
                )
            ),
            key_results_count=(
                additional_properties.get(
                    "keyResultsCount"
                )
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the Objective object to a dictionary.
        """
        return asdict(self)