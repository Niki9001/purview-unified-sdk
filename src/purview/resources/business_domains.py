from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlparse
from uuid import uuid4

from purview.models.business_domain import (
    BusinessDomain,
)
from purview.resources.base import (
    BaseResourceClient,
)


class BusinessDomainsClient(
    BaseResourceClient[BusinessDomain]
):
    """
    Client for Microsoft Purview Business Domain
    operations.

    This client targets Microsoft Purview Unified
    Catalog API version 2026-03-20-preview.
    """

    RESOURCE_PATH = "businessdomains"
    MODEL = BusinessDomain

    ALLOWED_DOMAIN_TYPES = {
        "FunctionalUnit",
        "LineOfBusiness",
        "DataDomain",
        "Regulatory",
        "Project",
    }

    ALLOWED_STATUSES = {
        "DRAFT",
        "PUBLISHED",
        "EXPIRED",
    }

    def enumerate_raw(
        self,
        *,
        skip_token: str | None = None,
        write_only: bool | None = None,
    ) -> dict[str, Any]:
        """
        Enumerate Business Domains and return the
        complete API response.

        Parameters
        ----------
        skip_token:
            Continuation token returned by the
            previous response.

        write_only:
            Whether to return only writable Business
            Domains.

        Returns
        -------
        dict[str, Any]
            Complete Purview API response, including
            pagination information.
        """
        params: dict[str, Any] = {}

        if skip_token is not None:
            params["$skipToken"] = self._validate_text(
                skip_token,
                field_name="skip_token",
            )

        if write_only is not None:
            if not isinstance(write_only, bool):
                raise TypeError(
                    "write_only must be a boolean."
                )

            params["writeOnly"] = write_only

        response = self.http.get(
            self.resource_path,
            params=params or None,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected Business Domain enumerate "
                "response to be a dictionary."
            )

        return response

    def enumerate(
        self,
        *,
        skip_token: str | None = None,
        write_only: bool | None = None,
    ) -> list[BusinessDomain]:
        """
        Enumerate Business Domains as model objects.
        """
        response = self.enumerate_raw(
            skip_token=skip_token,
            write_only=write_only,
        )

        return self._to_model_list(
            response,
            collection_key="value",
        )

    def list(
        self,
        *,
        skip_token: str | None = None,
        write_only: bool | None = None,
    ) -> list[BusinessDomain]:
        """
        Compatibility alias for enumerate().

        Microsoft Purview names this endpoint
        Enumerate Business Domains.
        """
        return self.enumerate(
            skip_token=skip_token,
            write_only=write_only,
        )

    def enumerate_all(
        self,
        *,
        write_only: bool | None = None,
    ) -> list[BusinessDomain]:
        """
        Retrieve all Business Domains across all
        result pages.
        """
        domains: list[BusinessDomain] = []
        skip_token: str | None = None
        seen_tokens: set[str] = set()

        while True:
            response = self.enumerate_raw(
                skip_token=skip_token,
                write_only=write_only,
            )

            domains.extend(
                self._to_model_list(
                    response,
                    collection_key="value",
                )
            )

            next_link = response.get("nextLink")

            if not next_link:
                break

            if not isinstance(next_link, str):
                raise TypeError(
                    "Expected nextLink to be a string."
                )

            next_token = self._extract_skip_token(
                next_link
            )

            if next_token is None:
                raise ValueError(
                    "The Business Domain response "
                    "contains nextLink but no "
                    "$skipToken parameter."
                )

            if next_token in seen_tokens:
                raise RuntimeError(
                    "Business Domain pagination "
                    "returned a repeated skip token."
                )

            seen_tokens.add(next_token)
            skip_token = next_token

        return domains

    def get(
        self,
        domain_id: str,
    ) -> BusinessDomain:
        """
        Get one Business Domain by UUID.
        """
        clean_domain_id = self._validate_uuid(
            domain_id,
            field_name="domain_id",
        )

        return super().get(
            clean_domain_id
        )

    def create(
        self,
        *,
        name: str,
        domain_type: str,
        description: str | None = None,
        status: str = "DRAFT",
        is_restricted: bool = False,
        domain_id: str | None = None,
        parent_id: str | None = None,
        domains: list[dict[str, Any]] | None = None,
        managed_attributes: list[dict[str, Any]]
        | None = None,
        system_data: dict[str, Any] | None = None,
        thumbnail: dict[str, Any] | None = None,
    ) -> BusinessDomain:
        """
        Create a Microsoft Purview Business Domain.

        The SDK requires the fields needed for a useful
        Business Domain and supports the remaining API
        fields as optional advanced parameters.

        Parameters
        ----------
        name:
            Name of the Business Domain.

        domain_type:
            Business Domain type.

            Supported values:
            - FunctionalUnit
            - LineOfBusiness
            - DataDomain
            - Regulatory
            - Project

        description:
            Optional description.

        status:
            Lifecycle status. Defaults to DRAFT.

        is_restricted:
            Whether access to the domain is restricted.

        domain_id:
            Optional Business Domain UUID. A UUID is
            generated when omitted.

        parent_id:
            Optional parent Business Domain UUID.

        domains:
            Optional platform-domain metadata.

        managed_attributes:
            Optional managed attributes.

        system_data:
            Optional system metadata. Normally this
            should be omitted and managed by Purview.

        thumbnail:
            Optional thumbnail metadata.

        Returns
        -------
        BusinessDomain
            The newly created Business Domain.
        """
        clean_domain_id = (
            self._validate_uuid(
                domain_id,
                field_name="domain_id",
            )
            if domain_id is not None
            else str(uuid4())
        )

        payload: dict[str, Any] = {
            "id": clean_domain_id,
            "name": self._validate_text(
                name,
                field_name="name",
            ),
            "type": self._validate_domain_type(
                domain_type
            ),
            "status": self._validate_status(
                status
            ),
        }

        if not isinstance(is_restricted, bool):
            raise TypeError(
                "is_restricted must be a boolean."
            )

        payload["isRestricted"] = is_restricted

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
                self._validate_uuid(
                    parent_id,
                    field_name="parent_id",
                )
            )

        if domains is not None:
            payload["domains"] = (
                self._validate_dict_list(
                    domains,
                    field_name="domains",
                )
            )

        if managed_attributes is not None:
            payload["managedAttributes"] = (
                self._validate_dict_list(
                    managed_attributes,
                    field_name="managed_attributes",
                )
            )

        if system_data is not None:
            payload["systemData"] = (
                self._validate_dictionary(
                    system_data,
                    field_name="system_data",
                )
            )

        if thumbnail is not None:
            payload["thumbnail"] = (
                self._validate_dictionary(
                    thumbnail,
                    field_name="thumbnail",
                )
            )

        return super().create(payload)
    
    def update(
        self,
        domain_id: str,
        *,
        domains: list[dict[str, Any]]
        | None = None,
        managed_attributes: list[
            dict[str, Any]
        ]
        | None = None,
        parent_id: str | None = None,
        system_data: dict[str, Any]
        | None = None,
        thumbnail: dict[str, Any]
        | None = None,
        name: str | None = None,
        domain_type: str | None = None,
        description: str | None = None,
        status: str | None = None,
        is_restricted: bool | None = None,
    ) -> BusinessDomain:
        """
        Update an existing Business Domain using PUT.

        Purview's update endpoint uses PUT. The current
        Business Domain is retrieved first, and all fields
        returned by Purview are preserved. Only fields
        explicitly supplied by the caller are replaced.

        This avoids requiring response properties that may
        be absent for some Business Domains or tenants.
        """
        clean_domain_id = self._validate_uuid(
            domain_id,
            field_name="domain_id",
        )

        if all(
            value is None
            for value in (
                domains,
                managed_attributes,
                parent_id,
                system_data,
                thumbnail,
                name,
                domain_type,
                description,
                status,
                is_restricted,
            )
        ):
            raise ValueError(
                "At least one field must be provided "
                "for update."
            )

        current_data = self.get_raw(
            clean_domain_id
        )

        if not isinstance(current_data, dict):
            raise TypeError(
                "Expected the existing Business "
                "Domain response to be a dictionary."
            )

        payload: dict[str, Any] = dict(
            current_data
        )

        # Keep the path ID and body ID consistent.
        payload["id"] = clean_domain_id

        if domains is not None:
            payload["domains"] = (
                self._validate_dict_list(
                    domains,
                    field_name="domains",
                )
            )

        if managed_attributes is not None:
            payload["managedAttributes"] = (
                self._validate_dict_list(
                    managed_attributes,
                    field_name=(
                        "managed_attributes"
                    ),
                )
            )

        if parent_id is not None:
            payload["parentId"] = (
                self._validate_uuid(
                    parent_id,
                    field_name="parent_id",
                )
            )

        if system_data is not None:
            payload["systemData"] = (
                self._validate_dictionary(
                    system_data,
                    field_name="system_data",
                )
            )

        if thumbnail is not None:
            payload["thumbnail"] = (
                self._validate_dictionary(
                    thumbnail,
                    field_name="thumbnail",
                )
            )

        if name is not None:
            payload["name"] = self._validate_text(
                name,
                field_name="name",
            )

        if domain_type is not None:
            payload["type"] = (
                self._validate_domain_type(
                    domain_type
                )
            )

        if description is not None:
            payload["description"] = (
                self._validate_optional_text(
                    description,
                    field_name="description",
                )
            )

        if status is not None:
            payload["status"] = (
                self._validate_status(status)
            )

        if is_restricted is not None:
            if not isinstance(
                is_restricted,
                bool,
            ):
                raise TypeError(
                    "is_restricted must be a "
                    "boolean."
                )

            payload["isRestricted"] = (
                is_restricted
            )

        response = self.http.put(
            self._item_path(
                clean_domain_id,
                field_name="domain_id",
            ),
            json=payload,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected Business Domain update "
                "response to be a dictionary."
            )

        return self._to_model(response)

    def delete(
        self,
        domain_id: str,
    ) -> Any:
        """
        Delete a Business Domain by UUID.
        """
        clean_domain_id = self._validate_uuid(
            domain_id,
            field_name="domain_id",
        )

        return super().delete(
            clean_domain_id
        )

    @classmethod
    def _validate_domain_type(
        cls,
        domain_type: str,
    ) -> str:
        """
        Validate a Business Domain type.
        """
        clean_domain_type = cls._validate_text(
            domain_type,
            field_name="domain_type",
        )

        if (
            clean_domain_type
            not in cls.ALLOWED_DOMAIN_TYPES
        ):
            allowed_values = ", ".join(
                sorted(
                    cls.ALLOWED_DOMAIN_TYPES
                )
            )

            raise ValueError(
                "domain_type must be one of: "
                f"{allowed_values}."
            )

        return clean_domain_type

    @classmethod
    def _validate_status(
        cls,
        status: str,
    ) -> str:
        """
        Validate a Business Domain lifecycle status.
        """
        clean_status = cls._validate_text(
            status,
            field_name="status",
        ).upper()

        if clean_status not in cls.ALLOWED_STATUSES:
            allowed_values = ", ".join(
                sorted(cls.ALLOWED_STATUSES)
            )

            raise ValueError(
                "status must be one of: "
                f"{allowed_values}."
            )

        return clean_status

    @classmethod
    def _validate_optional_text(
        cls,
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Validate an optional text value.

        Empty strings are allowed because some API
        fields can be intentionally cleared.
        """
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        return value.strip()

    @staticmethod
    def _validate_dictionary(
        value: dict[str, Any],
        *,
        field_name: str,
    ) -> dict[str, Any]:
        """
        Validate a dictionary request field.
        """
        if not isinstance(value, dict):
            raise TypeError(
                f"{field_name} must be a dictionary."
            )

        return value

    @staticmethod
    def _validate_dict_list(
        value: list[dict[str, Any]],
        *,
        field_name: str,
    ) -> list[dict[str, Any]]:
        """
        Validate a list containing dictionaries.
        """
        if not isinstance(value, list):
            raise TypeError(
                f"{field_name} must be a list."
            )

        for index, item in enumerate(value):
            if not isinstance(item, dict):
                raise TypeError(
                    f"{field_name}[{index}] must be "
                    "a dictionary."
                )

        return value

    @staticmethod
    def _extract_skip_token(
        next_link: str,
    ) -> str | None:
        """
        Extract the Business Domain $skipToken value
        from a pagination nextLink.
        """
        parsed_url = urlparse(next_link)
        query = parse_qs(
            parsed_url.query
        )

        token_values = (
            query.get("$skipToken")
            or query.get("skipToken")
        )

        if not token_values:
            return None

        token = token_values[0].strip()

        return token or None