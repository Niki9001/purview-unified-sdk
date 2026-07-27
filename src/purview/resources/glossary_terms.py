from __future__ import annotations

from typing import Any
from uuid import uuid4

from purview.models.glossary_term import GlossaryTerm
from purview.resources.base import BaseResourceClient


class GlossaryTermsClient(
    BaseResourceClient[GlossaryTerm]
):
    """
    Client for Microsoft Purview Glossary Term operations.
    """

    RESOURCE_PATH = "terms"

    MODEL = GlossaryTerm

    VALID_STATUSES = {
        "DRAFT",
        "PUBLISHED",
        "EXPIRED",
    }

    def _term_path(
        self,
        term_id: str,
    ) -> str:
        """
        Build the API path for a specific glossary term.
        """
        return (
            f"{self.RESOURCE_PATH}/{term_id}"
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
        Validate and normalize a glossary term status.
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
    def _validate_acronyms(
        cls,
        acronyms: list[str],
    ) -> list[str]:
        """
        Validate and normalize glossary term acronyms.
        """
        if not isinstance(acronyms, list):
            raise TypeError(
                "acronyms must be a list of strings."
            )

        clean_acronyms: list[str] = []

        for index, acronym in enumerate(acronyms):
            clean_acronym = cls._validate_text(
                acronym,
                field_name=f"acronyms[{index}]",
            )

            clean_acronyms.append(
                clean_acronym
            )

        return clean_acronyms

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
        Validate glossary term contacts.
        """
        if not isinstance(contacts, dict):
            raise TypeError(
                "contacts must be a dictionary."
            )

        return contacts

    @staticmethod
    def _validate_resources(
        resources: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        """
        Validate glossary term resources.
        """
        if not isinstance(resources, list):
            raise TypeError(
                "resources must be a list."
            )

        return resources

    @staticmethod
    def _validate_managed_attributes(
        managed_attributes: list[
            dict[str, Any]
        ],
    ) -> list[dict[str, Any]]:
        """
        Validate glossary term managed attributes.
        """
        if not isinstance(
            managed_attributes,
            list,
        ):
            raise TypeError(
                "managed_attributes must be a list."
            )

        return managed_attributes

    def create(
        self,
        *,
        name: str,
        domain_id: str,
        description: str | None = None,
        status: str = "DRAFT",
        term_id: str | None = None,
        parent_id: str | None = None,
        acronyms: list[str] | None = None,
        contacts: dict[
            str,
            list[dict[str, str]],
        ]
        | None = None,
        resources: list[dict[str, str]]
        | None = None,
        managed_attributes: list[
            dict[str, Any]
        ]
        | None = None,
        is_leaf: bool | None = None,
    ) -> GlossaryTerm:
        """
        Create a Microsoft Purview Glossary Term.

        Args:
            name:
                Display name of the glossary term.

            domain_id:
                ID of the Governance Domain where
                the term will be created.

            description:
                Optional description of the term.

            status:
                Lifecycle status. Supported values
                are DRAFT, PUBLISHED, and EXPIRED.

            term_id:
                Optional term UUID. A UUID is
                generated when omitted.

            parent_id:
                Optional parent glossary term ID.

            acronyms:
                Optional list of acronyms.

            contacts:
                Optional contact mapping.

            resources:
                Optional external resources.

            managed_attributes:
                Optional managed attributes.

            is_leaf:
                Optional leaf-node indicator.

        Returns:
            The newly created GlossaryTerm.
        """
        clean_name = self._validate_text(
            name,
            field_name="name",
        )

        clean_domain_id = self._validate_id(
            domain_id,
            field_name="domain_id",
        )

        clean_status = self._validate_status(
            status,
        )

        clean_term_id = (
            self._validate_id(
                term_id,
                field_name="term_id",
            )
            if term_id is not None
            else str(uuid4())
        )

        payload: dict[str, Any] = {
            "id": clean_term_id,
            "name": clean_name,
            "domain": clean_domain_id,
            "status": clean_status,
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

        if parent_id is not None:
            payload["parentId"] = (
                self._validate_id(
                    parent_id,
                    field_name="parent_id",
                )
            )

        if acronyms is not None:
            payload["acronyms"] = (
                self._validate_acronyms(
                    acronyms,
                )
            )

        if contacts is not None:
            payload["contacts"] = (
                self._validate_contacts(
                    contacts,
                )
            )

        if resources is not None:
            payload["resources"] = (
                self._validate_resources(
                    resources,
                )
            )

        if managed_attributes is not None:
            payload["managedAttributes"] = (
                self._validate_managed_attributes(
                    managed_attributes,
                )
            )

        if is_leaf is not None:
            if not isinstance(is_leaf, bool):
                raise TypeError(
                    "is_leaf must be a boolean "
                    "or None."
                )

            payload["isLeaf"] = is_leaf

        return super().create(payload)

    def list(
        self,
        *,
        skip: int | None = None,
        top: int | None = None,
        domain_id: str | None = None,
        parent_id: str | None = None,
        keyword: str | None = None,
        depth: int | None = None,
        order_by: str | None = None,
    ) -> list[GlossaryTerm]:
        """
        List glossary terms with optional filters.
        """
        params: dict[str, Any] = {}

        if skip is not None:
            if not isinstance(skip, int):
                raise TypeError(
                    "skip must be an integer."
                )

            if skip < 0:
                raise ValueError(
                    "skip cannot be negative."
                )

            params["skip"] = skip

        if top is not None:
            if not isinstance(top, int):
                raise TypeError(
                    "top must be an integer."
                )

            if top <= 0:
                raise ValueError(
                    "top must be greater than zero."
                )

            params["top"] = top

        if domain_id is not None:
            params["domainId"] = (
                self._validate_id(
                    domain_id,
                    field_name="domain_id",
                )
            )

        if parent_id is not None:
            params["parentId"] = (
                self._validate_id(
                    parent_id,
                    field_name="parent_id",
                )
            )

        if keyword is not None:
            params["keyword"] = (
                self._validate_text(
                    keyword,
                    field_name="keyword",
                )
            )

        if depth is not None:
            if not isinstance(depth, int):
                raise TypeError(
                    "depth must be an integer."
                )

            if depth < 0:
                raise ValueError(
                    "depth cannot be negative."
                )

            params["depth"] = depth

        if order_by is not None:
            params["orderBy"] = (
                self._validate_text(
                    order_by,
                    field_name="order_by",
                )
            )

        return super().list(
            params=params or None,
        )

    def update(
        self,
        term_id: str,
        *,
        name: str | None = None,
        domain_id: str | None = None,
        description: str | None = None,
        status: str | None = None,
        parent_id: str | None = None,
        acronyms: list[str] | None = None,
        contacts: dict[
            str,
            list[dict[str, str]],
        ]
        | None = None,
        resources: list[dict[str, str]]
        | None = None,
        managed_attributes: list[
            dict[str, Any]
        ]
        | None = None,
        is_leaf: bool | None = None,
    ) -> GlossaryTerm:
        """
        Update an existing Microsoft Purview
        Glossary Term.

        The update endpoint uses PUT and requires
        a complete payload. Existing values are
        retrieved before applying the requested
        changes.
        """
        clean_term_id = self._validate_id(
            term_id,
            field_name="term_id",
        )

        if all(
            value is None
            for value in (
                name,
                domain_id,
                description,
                status,
                parent_id,
                acronyms,
                contacts,
                resources,
                managed_attributes,
                is_leaf,
            )
        ):
            raise ValueError(
                "At least one field must be provided "
                "for the update."
            )

        current_data = self.http.get(
            self._term_path(clean_term_id),
        )

        if not isinstance(current_data, dict):
            raise TypeError(
                "Purview returned an unexpected "
                "glossary term response."
            )

        current_term = self.MODEL.from_dict(
            current_data
        )

        if not current_term.name:
            raise ValueError(
                "The existing glossary term does "
                "not contain a name."
            )

        if not current_term.domain_id:
            raise ValueError(
                "The existing glossary term does "
                "not contain a domain ID."
            )

        if not current_term.status:
            raise ValueError(
                "The existing glossary term does "
                "not contain a status."
            )

        payload: dict[str, Any] = {
            "id": clean_term_id,
            "name": current_term.name,
            "domain": current_term.domain_id,
            "status": current_term.status,
        }

        optional_api_fields = (
            "description",
            "parentId",
            "acronyms",
            "contacts",
            "resources",
            "managedAttributes",
            "isLeaf",
        )

        for field in optional_api_fields:
            if field in current_data:
                payload[field] = current_data[field]

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

        if description is not None:
            if not isinstance(description, str):
                raise TypeError(
                    "description must be a string "
                    "or None."
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

        if parent_id is not None:
            payload["parentId"] = (
                self._validate_id(
                    parent_id,
                    field_name="parent_id",
                )
            )

        if acronyms is not None:
            payload["acronyms"] = (
                self._validate_acronyms(
                    acronyms,
                )
            )

        if contacts is not None:
            payload["contacts"] = (
                self._validate_contacts(
                    contacts,
                )
            )

        if resources is not None:
            payload["resources"] = (
                self._validate_resources(
                    resources,
                )
            )

        if managed_attributes is not None:
            payload["managedAttributes"] = (
                self._validate_managed_attributes(
                    managed_attributes,
                )
            )

        if is_leaf is not None:
            if not isinstance(is_leaf, bool):
                raise TypeError(
                    "is_leaf must be a boolean "
                    "or None."
                )

            payload["isLeaf"] = is_leaf

        response_data = self.http.put(
            self._term_path(clean_term_id),
            json=payload,
        )

        if not isinstance(response_data, dict):
            raise TypeError(
                "Purview returned an unexpected "
                "update response."
            )

        return self.MODEL.from_dict(
            response_data
        )

        