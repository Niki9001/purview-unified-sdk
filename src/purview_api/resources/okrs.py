from __future__ import annotations

from datetime import date, datetime
from typing import Any
from uuid import uuid4

from purview_api.models.key_result import KeyResult
from purview_api.models.objective import Objective
from purview_api.resources.base import BaseResourceClient


class OkrsClient(
    BaseResourceClient[Objective]
):
    """
    Client for Microsoft Purview Objective and
    Key Result operations.
    """

    RESOURCE_PATH = "objectives"

    MODEL = Objective

    VALID_OBJECTIVE_STATUSES = {
        "Draft",
        "Published",
        "Closed",
    }

    VALID_KEY_RESULT_STATUSES = {
        "NotTracked",
        "OnTrack",
        "Behind",
        "AtRisk",
    }

    @staticmethod
    def _validate_text(
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Validate and normalize required text.
        """
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        clean_value = value.strip()

        if not clean_value:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        return clean_value

    @classmethod
    def _validate_objective_status(
        cls,
        status: str,
    ) -> str:
        """
        Validate an Objective lifecycle status.
        """
        clean_status = cls._validate_text(
            status,
            field_name="status",
        )

        normalized_statuses = {
            value.lower(): value
            for value in (
                cls.VALID_OBJECTIVE_STATUSES
            )
        }

        normalized = normalized_statuses.get(
            clean_status.lower()
        )

        if normalized is None:
            valid_values = ", ".join(
                sorted(
                    cls.VALID_OBJECTIVE_STATUSES
                )
            )

            raise ValueError(
                "status must be one of: "
                f"{valid_values}."
            )

        return normalized

    @classmethod
    def _validate_key_result_status(
        cls,
        status: str,
    ) -> str:
        """
        Validate a Key Result progress status.
        """
        clean_status = cls._validate_text(
            status,
            field_name="status",
        )

        normalized_statuses = {
            value.lower(): value
            for value in (
                cls.VALID_KEY_RESULT_STATUSES
            )
        }

        normalized = normalized_statuses.get(
            clean_status.lower()
        )

        if normalized is None:
            valid_values = ", ".join(
                sorted(
                    cls.VALID_KEY_RESULT_STATUSES
                )
            )

            raise ValueError(
                "status must be one of: "
                f"{valid_values}."
            )

        return normalized

    @staticmethod
    def _validate_number(
        value: int | float,
        *,
        field_name: str,
    ) -> float:
        """
        Validate a numeric Key Result value.
        """
        if isinstance(value, bool):
            raise TypeError(
                f"{field_name} must be a number."
            )

        if not isinstance(value, (int, float)):
            raise TypeError(
                f"{field_name} must be a number."
            )

        return float(value)

    @staticmethod
    def _validate_contacts(
        contacts: dict[
            str,
            list[dict[str, str]],
        ],
    ) -> dict[
        str,
        list[dict[str, str]],
    ]:
        """
        Validate Objective contacts.
        """
        if not isinstance(contacts, dict):
            raise TypeError(
                "contacts must be a dictionary."
            )

        valid_contact_types = {
            "owner",
            "expert",
            "databaseAdmin",
        }

        for contact_type, contact_list in (
            contacts.items()
        ):
            if contact_type not in valid_contact_types:
                valid_values = ", ".join(
                    sorted(valid_contact_types)
                )

                raise ValueError(
                    "contacts keys must be one of: "
                    f"{valid_values}."
                )

            if not isinstance(contact_list, list):
                raise TypeError(
                    f"contacts[{contact_type!r}] "
                    "must be a list."
                )

            for index, contact in enumerate(
                contact_list
            ):
                if not isinstance(contact, dict):
                    raise TypeError(
                        f"contacts[{contact_type!r}]"
                        f"[{index}] must be a "
                        "dictionary."
                    )

                contact_id = contact.get("id")

                if not isinstance(contact_id, str):
                    raise TypeError(
                        f"contacts[{contact_type!r}]"
                        f"[{index}]['id'] must be "
                        "a string."
                    )

                if not contact_id.strip():
                    raise ValueError(
                        f"contacts[{contact_type!r}]"
                        f"[{index}]['id'] cannot be "
                        "empty."
                    )

        return contacts

    @staticmethod
    def _normalize_target_date(
        target_date: str | date | datetime,
    ) -> str:
        """
        Convert a target date to an ISO-8601 string.
        """
        if isinstance(target_date, datetime):
            return target_date.isoformat()

        if isinstance(target_date, date):
            return datetime.combine(
                target_date,
                datetime.min.time(),
            ).isoformat()

        if isinstance(target_date, str):
            clean_value = target_date.strip()

            if not clean_value:
                raise ValueError(
                    "target_date cannot be empty."
                )

            return clean_value

        raise TypeError(
            "target_date must be a string, date, "
            "or datetime."
        )

    def _objective_path(
        self,
        objective_id: str,
    ) -> str:
        """
        Build the path for one Objective.
        """
        return (
            f"{self.RESOURCE_PATH}/{objective_id}"
        )

    def _key_results_path(
        self,
        objective_id: str,
    ) -> str:
        """
        Build the Key Results collection path.
        """
        return (
            f"{self._objective_path(objective_id)}"
            "/keyResults"
        )

    def _key_result_path(
        self,
        objective_id: str,
        key_result_id: str,
    ) -> str:
        """
        Build the path for one Key Result.
        """
        return (
            f"{self._key_results_path(objective_id)}"
            f"/{key_result_id}"
        )

    def create_objective(
        self,
        *,
        definition: str,
        domain_id: str,
        target_date: str | date | datetime
        | None = None,
        status: str = "Draft",
        objective_id: str | None = None,
        contacts: dict[
            str,
            list[dict[str, str]],
        ]
        | None = None,
    ) -> Objective:
        """
        Create a Microsoft Purview Objective.
        """
        clean_definition = self._validate_text(
            definition,
            field_name="definition",
        )

        clean_domain_id = self._validate_id(
            domain_id,
            field_name="domain_id",
        )

        clean_status = (
            self._validate_objective_status(
                status
            )
        )

        clean_objective_id = (
            self._validate_id(
                objective_id,
                field_name="objective_id",
            )
            if objective_id is not None
            else str(uuid4())
        )

        payload: dict[str, Any] = {
            "id": clean_objective_id,
            "definition": clean_definition,
            "domain": clean_domain_id,
            "status": clean_status,
            "contacts": {},
        }

        if target_date is not None:
            payload["targetDate"] = (
                self._normalize_target_date(
                    target_date
                )
            )

        if contacts is not None:
            payload["contacts"] = (
                self._validate_contacts(
                    contacts
                )
            )

        response = self.http.post(
            self.resource_path,
            json=payload,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected Objective response to "
                "be a dictionary."
            )

        return Objective.from_dict(response)

    def update_objective(
        self,
        objective_id: str,
        *,
        definition: str | None = None,
        domain_id: str | None = None,
        target_date: str | date | datetime
        | None = None,
        status: str | None = None,
        contacts: dict[
            str,
            list[dict[str, str]],
        ]
        | None = None,
    ) -> Objective:
        """
        Update an existing Microsoft Purview Objective.

        The update endpoint uses PUT. Existing values
        are retrieved before applying the requested
        changes.
        """
        clean_objective_id = self._validate_id(
            objective_id,
            field_name="objective_id",
        )

        if all(
            value is None
            for value in (
                definition,
                domain_id,
                target_date,
                status,
                contacts,
            )
        ):
            raise ValueError(
                "At least one field must be provided "
                "for the update."
            )

        current_data = self.http.get(
            self._objective_path(
                clean_objective_id
            )
        )

        if not isinstance(current_data, dict):
            raise TypeError(
                "Purview returned an unexpected "
                "Objective response."
            )

        current_objective = Objective.from_dict(
            current_data
        )

        if not current_objective.definition:
            raise ValueError(
                "The existing Objective does not "
                "contain a definition."
            )

        if not current_objective.domain_id:
            raise ValueError(
                "The existing Objective does not "
                "contain a domain ID."
            )

        if not current_objective.status:
            raise ValueError(
                "The existing Objective does not "
                "contain a status."
            )

        payload: dict[str, Any] = {
            "id": clean_objective_id,
            "definition": (
                current_objective.definition
            ),
            "domain": current_objective.domain_id,
            "status": current_objective.status,
            "contacts": current_data.get(
                "contacts",
                {},
            ),
        }

        if current_objective.target_date is not None:
            payload["targetDate"] = (
                current_objective.target_date
            )

        if definition is not None:
            payload["definition"] = (
                self._validate_text(
                    definition,
                    field_name="definition",
                )
            )

        if domain_id is not None:
            payload["domain"] = self._validate_id(
                domain_id,
                field_name="domain_id",
            )

        if target_date is not None:
            payload["targetDate"] = (
                self._normalize_target_date(
                    target_date
                )
            )

        if status is not None:
            payload["status"] = (
                self._validate_objective_status(
                    status
                )
            )

        if contacts is not None:
            payload["contacts"] = (
                self._validate_contacts(
                    contacts
                )
            )

        response = self.http.put(
            self._objective_path(
                clean_objective_id
            ),
            json=payload,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Purview returned an unexpected "
                "Objective update response."
            )

        return Objective.from_dict(response)

    def create_key_result(
        self,
        *,
        objective_id: str,
        domain_id: str,
        definition: str,
        progress: int | float,
        goal: int | float,
        max_value: int | float,
        status: str = "NotTracked",
        key_result_id: str | None = None,
    ) -> KeyResult:
        """
        Create a Key Result under an Objective.
        """
        clean_objective_id = self._validate_id(
            objective_id,
            field_name="objective_id",
        )

        clean_domain_id = self._validate_id(
            domain_id,
            field_name="domain_id",
        )

        clean_definition = self._validate_text(
            definition,
            field_name="definition",
        )

        clean_status = (
            self._validate_key_result_status(
                status
            )
        )

        clean_key_result_id = (
            self._validate_id(
                key_result_id,
                field_name="key_result_id",
            )
            if key_result_id is not None
            else str(uuid4())
        )

        clean_progress = self._validate_number(
            progress,
            field_name="progress",
        )

        clean_goal = self._validate_number(
            goal,
            field_name="goal",
        )

        clean_max = self._validate_number(
            max_value,
            field_name="max_value",
        )

        if clean_max < clean_goal:
            raise ValueError(
                "max_value cannot be less than goal."
            )

        payload: dict[str, Any] = {
            "id": clean_key_result_id,
            "domainId": clean_domain_id,
            "definition": clean_definition,
            "progress": clean_progress,
            "goal": clean_goal,
            "max": clean_max,
            "status": clean_status,
        }

        response = self.http.post(
            self._key_results_path(
                clean_objective_id
            ),
            json=payload,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected Key Result response to "
                "be a dictionary."
            )

        return KeyResult.from_dict(response)

    def get_objective(
        self,
        objective_id: str,
    ) -> Objective:
        """
        Retrieve one Objective by ID.
        """
        clean_objective_id = self._validate_id(
            objective_id,
            field_name="objective_id",
        )

        response = self.http.get(
            self._objective_path(
                clean_objective_id
            )
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected Objective response to "
                "be a dictionary."
            )

        return Objective.from_dict(response)

    def get_key_result(
        self,
        objective_id: str,
        key_result_id: str,
    ) -> KeyResult:
        """
        Retrieve one Key Result.
        """
        clean_objective_id = self._validate_id(
            objective_id,
            field_name="objective_id",
        )

        clean_key_result_id = self._validate_id(
            key_result_id,
            field_name="key_result_id",
        )

        response = self.http.get(
            self._key_result_path(
                clean_objective_id,
                clean_key_result_id,
            )
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected Key Result response to "
                "be a dictionary."
            )

        return KeyResult.from_dict(response)

    def list_key_results(
        self,
        objective_id: str,
    ) -> list[KeyResult]:
        """
        List Key Results under one Objective.
        """
        clean_objective_id = self._validate_id(
            objective_id,
            field_name="objective_id",
        )

        response = self.http.get(
            self._key_results_path(
                clean_objective_id
            )
        )

        if isinstance(response, list):
            items = response
        elif isinstance(response, dict):
            items = (
                response.get("value")
                or response.get("items")
                or []
            )
        else:
            raise TypeError(
                "Expected Key Result list response."
            )

        return [
            KeyResult.from_dict(item)
            for item in items
            if isinstance(item, dict)
        ]

    def delete_objective(
        self,
        objective_id: str,
    ) -> None:
        """
        Delete an Objective.
        """
        clean_objective_id = self._validate_id(
            objective_id,
            field_name="objective_id",
        )

        self.http.delete(
            self._objective_path(
                clean_objective_id
            )
        )

    def delete_key_result(
        self,
        objective_id: str,
        key_result_id: str,
    ) -> None:
        """
        Delete a Key Result from an Objective.
        """
        clean_objective_id = self._validate_id(
            objective_id,
            field_name="objective_id",
        )

        clean_key_result_id = self._validate_id(
            key_result_id,
            field_name="key_result_id",
        )

        self.http.delete(
            self._key_result_path(
                clean_objective_id,
                clean_key_result_id,
            )
        )