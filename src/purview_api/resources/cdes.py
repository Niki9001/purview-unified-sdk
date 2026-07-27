from __future__ import annotations

from typing import Any
from uuid import uuid4

from purview_api.models.critical_data_element import (
    CriticalDataElement,
)
from purview_api.resources.base import BaseResourceClient


class CriticalDataElementsClient(
    BaseResourceClient[CriticalDataElement]
):
    """
    Client for Microsoft Purview Critical Data
    Element operations.
    """

    RESOURCE_PATH = "criticalDataElements"

    MODEL = CriticalDataElement

    VALID_STATUSES = {
        "DRAFT",
        "PUBLISHED",
        "EXPIRED",
    }

    VALID_DATA_TYPES = {
        "TEXT",
        "NUMBER",
        "DATETIME",
        "BOOLEAN",
    }

    def _cde_path(
        self,
        cde_id: str,
    ) -> str:
        """
        Build the API path for a specific Critical
        Data Element.
        """
        return (
            f"{self.RESOURCE_PATH}/{cde_id}"
        )

    @staticmethod
    def _validate_text(
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Validate and normalize a required text value.
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
    def _validate_status(
        cls,
        status: str,
    ) -> str:
        """
        Validate and normalize a CDE status.
        """
        clean_status = cls._validate_text(
            status,
            field_name="status",
        ).upper()

        if clean_status not in cls.VALID_STATUSES:
            valid_values = ", ".join(
                sorted(cls.VALID_STATUSES)
            )

            raise ValueError(
                "status must be one of: "
                f"{valid_values}."
            )

        return clean_status

    @classmethod
    def _validate_data_type(
        cls,
        data_type: str,
    ) -> str:
        """
        Validate and normalize a CDE data type.
        """
        clean_data_type = cls._validate_text(
            data_type,
            field_name="data_type",
        ).upper()

        if clean_data_type not in cls.VALID_DATA_TYPES:
            valid_values = ", ".join(
                sorted(cls.VALID_DATA_TYPES)
            )

            raise ValueError(
                "data_type must be one of: "
                f"{valid_values}."
            )

        return clean_data_type

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
        Validate CDE contacts.
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

                if contact_id is None:
                    raise ValueError(
                        f"contacts[{contact_type!r}]"
                        f"[{index}] must contain "
                        "an id."
                    )

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

                description = contact.get(
                    "description"
                )

                if (
                    description is not None
                    and not isinstance(
                        description,
                        str,
                    )
                ):
                    raise TypeError(
                        f"contacts[{contact_type!r}]"
                        f"[{index}]['description'] "
                        "must be a string or None."
                    )

        return contacts

    @staticmethod
    def _validate_managed_attributes(
        managed_attributes: list[
            dict[str, Any]
        ],
    ) -> list[dict[str, Any]]:
        """
        Validate CDE managed attributes.
        """
        if not isinstance(
            managed_attributes,
            list,
        ):
            raise TypeError(
                "managed_attributes must be a list."
            )

        for index, attribute in enumerate(
            managed_attributes
        ):
            if not isinstance(attribute, dict):
                raise TypeError(
                    f"managed_attributes[{index}] "
                    "must be a dictionary."
                )

            name = attribute.get("name")

            if name is None:
                raise ValueError(
                    f"managed_attributes[{index}] "
                    "must contain a name."
                )

            if not isinstance(name, str):
                raise TypeError(
                    f"managed_attributes[{index}]"
                    "['name'] must be a string."
                )

            if not name.strip():
                raise ValueError(
                    f"managed_attributes[{index}]"
                    "['name'] cannot be empty."
                )

            value = attribute.get("value")

            if (
                value is not None
                and not isinstance(value, str)
            ):
                raise TypeError(
                    f"managed_attributes[{index}]"
                    "['value'] must be a string "
                    "or None."
                )

            is_required = attribute.get(
                "isRequired"
            )

            if (
                is_required is not None
                and not isinstance(
                    is_required,
                    bool,
                )
            ):
                raise TypeError(
                    f"managed_attributes[{index}]"
                    "['isRequired'] must be a "
                    "boolean or None."
                )

        return managed_attributes

    def create(
        self,
        *,
        name: str,
        domain_id: str,
        data_type: str,
        description: str | None = None,
        status: str = "DRAFT",
        cde_id: str | None = None,
        contacts: dict[
            str,
            list[dict[str, str]],
        ]
        | None = None,
        managed_attributes: list[
            dict[str, Any]
        ]
        | None = None,
    ) -> CriticalDataElement:
        """
        Create a Microsoft Purview Critical Data
        Element.

        Args:
            name:
                Name of the Critical Data Element.

            domain_id:
                ID of the Governance Domain where
                the CDE will be created.

            data_type:
                Data type of the CDE. Supported
                values are TEXT, NUMBER, DATETIME,
                and BOOLEAN.

            description:
                Optional description of the CDE.

            status:
                Lifecycle status. Supported values
                are DRAFT, PUBLISHED, and EXPIRED.

            cde_id:
                Optional CDE UUID. A new UUID is
                generated when omitted.

            contacts:
                Optional contact mapping. Supported
                contact keys are owner, expert, and
                databaseAdmin.

            managed_attributes:
                Optional managed attributes.

        Returns:
            The newly created CriticalDataElement.
        """
        clean_name = self._validate_text(
            name,
            field_name="name",
        )

        clean_domain_id = self._validate_id(
            domain_id,
            field_name="domain_id",
        )

        clean_data_type = (
            self._validate_data_type(
                data_type,
            )
        )

        clean_status = self._validate_status(
            status,
        )

        clean_cde_id = (
            self._validate_id(
                cde_id,
                field_name="cde_id",
            )
            if cde_id is not None
            else str(uuid4())
        )

        payload: dict[str, Any] = {
            "id": clean_cde_id,
            "name": clean_name,
            "domain": clean_domain_id,
            "dataType": clean_data_type,
            "status": clean_status,
            "contacts": {},
        }

        if description is not None:
            if not isinstance(description, str):
                raise TypeError(
                    "description must be a string "
                    "or None."
                )

            payload["description"] = (
                description.strip()
            )

        if contacts is not None:
            payload["contacts"] = (
                self._validate_contacts(
                    contacts,
                )
            )

        if managed_attributes is not None:
            payload["managedAttributes"] = (
                self._validate_managed_attributes(
                    managed_attributes,
                )
            )

        return super().create(payload)

    def update(
        self,
        cde_id: str,
        *,
        name: str | None = None,
        domain_id: str | None = None,
        data_type: str | None = None,
        description: str | None = None,
        status: str | None = None,
        contacts: dict[
            str,
            list[dict[str, str]],
        ]
        | None = None,
        managed_attributes: list[
            dict[str, Any]
        ]
        | None = None,
    ) -> CriticalDataElement:
        """
        Update an existing Microsoft Purview
        Critical Data Element.

        The update endpoint uses PUT. Existing values
        are retrieved before applying the requested
        changes.
        """
        clean_cde_id = self._validate_id(
            cde_id,
            field_name="cde_id",
        )

        if all(
            value is None
            for value in (
                name,
                domain_id,
                data_type,
                description,
                status,
                contacts,
                managed_attributes,
            )
        ):
            raise ValueError(
                "At least one field must be provided "
                "for the update."
            )

        current_data = self.http.get(
            self._cde_path(clean_cde_id),
        )

        if not isinstance(current_data, dict):
            raise TypeError(
                "Purview returned an unexpected "
                "Critical Data Element response."
            )

        current_cde = self.MODEL.from_dict(
            current_data
        )

        if not current_cde.name:
            raise ValueError(
                "The existing CDE does not contain "
                "a name."
            )

        if not current_cde.domain_id:
            raise ValueError(
                "The existing CDE does not contain "
                "a domain ID."
            )

        if not current_cde.data_type:
            raise ValueError(
                "The existing CDE does not contain "
                "a data type."
            )

        if not current_cde.status:
            raise ValueError(
                "The existing CDE does not contain "
                "a status."
            )

        payload: dict[str, Any] = {
            "id": clean_cde_id,
            "name": current_cde.name,
            "domain": current_cde.domain_id,
            "dataType": current_cde.data_type,
            "status": current_cde.status,
            "contacts": current_data.get(
                "contacts",
                {},
            ),
        }

        if current_cde.description is not None:
            payload["description"] = (
                current_cde.description
            )

        if "managedAttributes" in current_data:
            payload["managedAttributes"] = (
                current_data["managedAttributes"]
            )

        if name is not None:
            payload["name"] = self._validate_text(
                name,
                field_name="name",
            )

        if domain_id is not None:
            payload["domain"] = self._validate_id(
                domain_id,
                field_name="domain_id",
            )

        if data_type is not None:
            payload["dataType"] = (
                self._validate_data_type(
                    data_type,
                )
            )

        if description is not None:
            if not isinstance(description, str):
                raise TypeError(
                    "description must be a string."
                )

            payload["description"] = (
                description.strip()
            )

        if status is not None:
            payload["status"] = (
                self._validate_status(
                    status,
                )
            )

        if contacts is not None:
            payload["contacts"] = (
                self._validate_contacts(
                    contacts,
                )
            )

        if managed_attributes is not None:
            payload["managedAttributes"] = (
                self._validate_managed_attributes(
                    managed_attributes,
                )
            )

        response_data = self.http.put(
            self._cde_path(clean_cde_id),
            json=payload,
        )

        if not isinstance(response_data, dict):
            raise TypeError(
                "Purview returned an unexpected "
                "CDE update response."
            )

        return self.MODEL.from_dict(
            response_data
        )

    def query(
        self,
        payload: dict[str, Any] | None = None,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Query Critical Data Elements and return the
        raw API response.

        Use this method when pagination metadata or
        the full Purview response is needed.
        """
        request_payload = (
            payload
            if payload is not None
            else {}
        )

        response = self.http.post(
            f"{self.resource_path}/query",
            params=params,
            json=request_payload,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected CDE query response to be "
                "a dictionary."
            )

        return response

    def query_models(
        self,
        payload: dict[str, Any] | None = None,
        *,
        params: dict[str, Any] | None = None,
    ) -> list[CriticalDataElement]:
        """
        Query Critical Data Elements and return
        model objects.

        Pagination metadata is not included in the
        returned list. Use query() when the complete
        response is needed.
        """
        response = self.query(
            payload=payload,
            params=params,
        )

        return self._to_model_list(response)