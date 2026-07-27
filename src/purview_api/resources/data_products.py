from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from purview_api.models.data_product import DataProduct
from purview_api.resources.base import BaseResourceClient


class DataProductsClient(
    BaseResourceClient[DataProduct]
):
    """
    Client for Microsoft Purview Data Product operations.
    """

    RESOURCE_PATH = "dataProducts"
    MODEL = DataProduct

    ALLOWED_STATUSES = {
        "DRAFT",
        "PUBLISHED",
        "EXPIRED",
    }

    ALLOWED_DATA_PRODUCT_TYPES = {
        "Master",
        "Reference",
        "Analytical",
        "AI",
        "MasterDataAndReferenceData",
        "BusinessSystemOrApplication",
        "ModelTypes",
        "DashboardsOrReports",
        "Operational",
        "MLAITrainingDataSet",
        "MLAITestingDataSet",
        "TransactionalDataset",
        "AnalyticsModel",
        "SemanticModel",
    }

    ALLOWED_UPDATE_FREQUENCIES = {
        "Hourly",
        "Daily",
        "Weekly",
        "Monthly",
        "Quarterly",
        "Yearly",
    }

    ALLOWED_CONTACT_TYPES = {
        "owner",
        "expert",
        "databaseAdmin",
    }

    def list(
        self,
        *,
        domain_id: str | None = None,
        skip: int | None = None,
        top: int | None = None,
        order_by: str | None = None,
    ) -> list[DataProduct]:
        """
        List Data Products.

        Parameters
        ----------
        domain_id:
            Optional Business Domain ID filter.

        skip:
            Number of Data Products to skip.

        top:
            Maximum number of Data Products to return.

        order_by:
            Optional API sorting expression.

        Returns
        -------
        list[DataProduct]
            Data Products returned by Microsoft Purview.
        """
        params: dict[str, Any] = {}

        if domain_id is not None:
            params["domainId"] = self._validate_uuid(
                domain_id,
                field_name="domain_id",
            )

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

        if order_by is not None:
            if not isinstance(order_by, str):
                raise TypeError(
                    "order_by must be a string."
                )

            clean_order_by = order_by.strip()

            if not clean_order_by:
                raise ValueError(
                    "order_by cannot be empty."
                )

            params["orderBy"] = clean_order_by

        return super().list(
            params=params or None,
        )

    def create(
        self,
        *,
        name: str,
        domain_id: str,
        contacts: dict[str, Any],
        data_product_type: str = "Master",
        status: str = "DRAFT",
        description: str | None = None,
        business_use: str | None = None,
        update_frequency: str | None = None,
        data_product_id: str | None = None,
        terms_of_use: list[Any] | None = None,
        documentation: list[Any] | None = None,
        managed_attributes: list[Any] | None = None,
        audience: list[str] | None = None,
        sensitivity_label: str | None = None,
        endorsed: bool | None = None,
    ) -> DataProduct:
        """
        Create a Data Product.
        """
        clean_name = self._validate_name(name)

        clean_domain_id = self._validate_uuid(
            domain_id,
            field_name="domain_id",
        )

        clean_contacts = self._validate_contacts(
            contacts
        )

        clean_type = self._validate_data_product_type(
            data_product_type
        )

        clean_status = self._validate_status(
            status
        )

        if data_product_id is None:
            clean_data_product_id = str(uuid4())
        else:
            clean_data_product_id = self._validate_uuid(
                data_product_id,
                field_name="data_product_id",
            )

        payload: dict[str, Any] = {
            "id": clean_data_product_id,
            "name": clean_name,
            "domain": clean_domain_id,
            "type": clean_type,
            "status": clean_status,
            "contacts": clean_contacts,
        }

        if description is not None:
            payload["description"] = (
                self._validate_optional_text(
                    description,
                    field_name="description",
                )
            )

        if business_use is not None:
            payload["businessUse"] = (
                self._validate_optional_text(
                    business_use,
                    field_name="business_use",
                )
            )

        if update_frequency is not None:
            payload["updateFrequency"] = (
                self._validate_update_frequency(
                    update_frequency
                )
            )

        if terms_of_use is not None:
            payload["termsOfUse"] = self._validate_list(
                terms_of_use,
                field_name="terms_of_use",
            )

        if documentation is not None:
            payload["documentation"] = self._validate_list(
                documentation,
                field_name="documentation",
            )

        if managed_attributes is not None:
            payload["managedAttributes"] = (
                self._validate_list(
                    managed_attributes,
                    field_name="managed_attributes",
                )
            )

        if audience is not None:
            payload["audience"] = (
                self._validate_audience(audience)
            )

        if sensitivity_label is not None:
            payload["sensitivityLabel"] = (
                self._validate_optional_text(
                    sensitivity_label,
                    field_name="sensitivity_label",
                )
            )

        if endorsed is not None:
            if not isinstance(endorsed, bool):
                raise TypeError(
                    "endorsed must be a boolean."
                )

            payload["endorsed"] = endorsed

        return super().create(payload)

    def update(
        self,
        data_product_id: str,
        *,
        name: str | None = None,
        domain_id: str | None = None,
        description: str | None = None,
        business_use: str | None = None,
        update_frequency: str | None = None,
        status: str | None = None,
        data_product_type: str | None = None,
        contacts: dict[str, Any] | None = None,
        terms_of_use: list[Any] | None = None,
        documentation: list[Any] | None = None,
        managed_attributes: list[Any] | None = None,
        audience: list[str] | None = None,
        sensitivity_label: str | None = None,
        endorsed: bool | None = None,
    ) -> DataProduct:
        """
        Update an existing Data Product using PUT.

        The current Data Product is retrieved first so existing
        properties can be preserved when they are not being changed.

        Parameters
        ----------
        data_product_id:
            ID of the Data Product to update.

        domain_id:
            Optional new Business Domain ID.

        name:
            Optional new Data Product name.

        description:
            Optional new description.

        business_use:
            Optional new business-use description.

        update_frequency:
            Optional new update frequency.

        status:
            Optional new lifecycle status.

        data_product_type:
            Optional new Data Product type.

        contacts:
            Optional replacement contacts map.

        Returns
        -------
        DataProduct
            The updated Data Product.
        """
        clean_data_product_id = self._validate_uuid(
            data_product_id,
            field_name="data_product_id",
        )

        if all(
            value is None
            for value in (
                name,
                domain_id,
                description,
                business_use,
                update_frequency,
                status,
                data_product_type,
                contacts,
                terms_of_use,
                documentation,
                managed_attributes,
                audience,
                sensitivity_label,
                endorsed,
            )
        ):
            raise ValueError(
                "At least one field must be provided "
                "for update."
            )

        current_data_product = self.get_raw(
            clean_data_product_id
        )

        if not isinstance(current_data_product, dict):
            raise TypeError(
                "Expected the existing Data Product "
                "response to be a dictionary."
            )

        payload: dict[str, Any] = dict(
            current_data_product
        )

        # The PUT API requires the Data Product ID in the body.
        payload["id"] = clean_data_product_id

        if name is not None:
            payload["name"] = self._validate_name(
                name
            )

        if domain_id is not None:
            payload["domain"] = self._validate_uuid(
                domain_id,
                field_name="domain_id",
            )

        if description is not None:
            payload["description"] = (
                self._validate_optional_text(
                    description,
                    field_name="description",
                )
            )

        if business_use is not None:
            payload["businessUse"] = (
                self._validate_optional_text(
                    business_use,
                    field_name="business_use",
                )
            )

        if update_frequency is not None:
            payload["updateFrequency"] = (
                self._validate_update_frequency(
                    update_frequency
                )
            )

        if status is not None:
            payload["status"] = self._validate_status(
                status
            )
        elif isinstance(payload.get("status"), str):
            payload["status"] = self._validate_status(
                payload["status"]
            )

        if data_product_type is not None:
            payload["type"] = (
                self._validate_data_product_type(
                    data_product_type
                )
            )
        elif isinstance(payload.get("type"), str):
            payload["type"] = (
                self._validate_data_product_type(
                    payload["type"]
                )
            )

        if contacts is not None:
            payload["contacts"] = (
                self._validate_contacts(contacts)
            )
        else:
            current_contacts = payload.get("contacts")

            if not isinstance(current_contacts, dict):
                raise ValueError(
                    "The existing Data Product does not "
                    "contain valid contacts."
                )

            payload["contacts"] = (
                self._validate_contacts(
                    current_contacts
                )
            )

        if terms_of_use is not None:
            payload["termsOfUse"] = self._validate_list(
                terms_of_use,
                field_name="terms_of_use",
            )

        if documentation is not None:
            payload["documentation"] = self._validate_list(
                documentation,
                field_name="documentation",
            )

        if managed_attributes is not None:
            payload["managedAttributes"] = (
                self._validate_list(
                    managed_attributes,
                    field_name="managed_attributes",
                )
            )

        if audience is not None:
            payload["audience"] = (
                self._validate_audience(audience)
            )

        if sensitivity_label is not None:
            payload["sensitivityLabel"] = (
                self._validate_optional_text(
                    sensitivity_label,
                    field_name="sensitivity_label",
                )
            )

        if endorsed is not None:
            if not isinstance(endorsed, bool):
                raise TypeError(
                    "endorsed must be a boolean."
                )

            payload["endorsed"] = endorsed

        current_name = payload.get("name")

        if not isinstance(current_name, str):
            raise ValueError(
                "The existing Data Product does not "
                "contain a valid name."
            )

        payload["name"] = self._validate_name(
            current_name
        )

        return super().put(
            clean_data_product_id,
            payload,
        )

    def delete(
        self,
        data_product_id: str,
    ) -> Any:
        """
        Delete a Data Product.
        """
        clean_data_product_id = self._validate_uuid(
            data_product_id,
            field_name="data_product_id",
        )

        return super().delete(
            clean_data_product_id
        )

    @staticmethod
    def _validate_name(
        name: str,
    ) -> str:
        """
        Validate and normalize a Data Product name.
        """
        if not isinstance(name, str):
            raise TypeError(
                "name must be a string."
            )

        clean_name = name.strip()

        if not clean_name:
            raise ValueError(
                "name cannot be empty."
            )

        return clean_name

    @staticmethod
    def _validate_uuid(
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Validate and normalize a UUID string.
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

        try:
            return str(UUID(clean_value))
        except ValueError as error:
            raise ValueError(
                f"{field_name} must be a valid UUID."
            ) from error

    @classmethod
    def _validate_contacts(
        cls,
        contacts: dict[str, Any],
    ) -> dict[str, list[dict[str, str]]]:
        """
        Validate Data Product contacts.
        """
        if not isinstance(contacts, dict):
            raise TypeError(
                "contacts must be a dictionary."
            )

        if not contacts:
            raise ValueError(
                "contacts cannot be empty."
            )

        clean_contacts: dict[
            str,
            list[dict[str, str]],
        ] = {}

        total_contacts = 0

        for contact_type, contact_items in contacts.items():
            if contact_type not in cls.ALLOWED_CONTACT_TYPES:
                allowed_values = ", ".join(
                    sorted(cls.ALLOWED_CONTACT_TYPES)
                )

                raise ValueError(
                    "Contact type must be one of: "
                    f"{allowed_values}."
                )

            if not isinstance(contact_items, list):
                raise TypeError(
                    f"contacts['{contact_type}'] "
                    "must be a list."
                )

            if not contact_items:
                raise ValueError(
                    f"contacts['{contact_type}'] "
                    "cannot be empty."
                )

            clean_items: list[dict[str, str]] = []

            for index, contact in enumerate(
                contact_items
            ):
                if not isinstance(contact, dict):
                    raise TypeError(
                        f"contacts['{contact_type}']"
                        f"[{index}] must be a dictionary."
                    )

                contact_id = contact.get("id")

                if contact_id is None:
                    raise ValueError(
                        f"contacts['{contact_type}']"
                        f"[{index}] must contain an id."
                    )

                clean_contact_id = cls._validate_uuid(
                    contact_id,
                    field_name=(
                        f"{contact_type} contact id"
                    ),
                )

                clean_contact: dict[str, str] = {
                    "id": clean_contact_id,
                }

                description = contact.get(
                    "description"
                )

                if description is not None:
                    clean_contact["description"] = (
                        cls._validate_optional_text(
                            description,
                            field_name=(
                                f"{contact_type} "
                                "contact description"
                            ),
                        )
                    )

                clean_items.append(clean_contact)
                total_contacts += 1

            clean_contacts[contact_type] = clean_items

        if total_contacts == 0:
            raise ValueError(
                "contacts must contain at least "
                "one contact."
            )

        return clean_contacts

    @classmethod
    def _validate_status(
        cls,
        status: str,
    ) -> str:
        """
        Validate a Data Product lifecycle status.
        """
        if not isinstance(status, str):
            raise TypeError(
                "status must be a string."
            )

        clean_status = status.strip().upper()

        if not clean_status:
            raise ValueError(
                "status cannot be empty."
            )

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
    def _validate_data_product_type(
        cls,
        data_product_type: str,
    ) -> str:
        """
        Validate a Data Product type.
        """
        if not isinstance(data_product_type, str):
            raise TypeError(
                "data_product_type must be a string."
            )

        clean_type = data_product_type.strip()

        if not clean_type:
            raise ValueError(
                "data_product_type cannot be empty."
            )

        if (
            clean_type
            not in cls.ALLOWED_DATA_PRODUCT_TYPES
        ):
            allowed_values = ", ".join(
                sorted(
                    cls.ALLOWED_DATA_PRODUCT_TYPES
                )
            )

            raise ValueError(
                "data_product_type must be one of: "
                f"{allowed_values}."
            )

        return clean_type

    @classmethod
    def _validate_update_frequency(
        cls,
        update_frequency: str,
    ) -> str:
        """
        Validate a Data Product update frequency.
        """
        if not isinstance(update_frequency, str):
            raise TypeError(
                "update_frequency must be a string."
            )

        clean_frequency = update_frequency.strip()

        if not clean_frequency:
            raise ValueError(
                "update_frequency cannot be empty."
            )

        if (
            clean_frequency
            not in cls.ALLOWED_UPDATE_FREQUENCIES
        ):
            allowed_values = ", ".join(
                sorted(
                    cls.ALLOWED_UPDATE_FREQUENCIES
                )
            )

            raise ValueError(
                "update_frequency must be one of: "
                f"{allowed_values}."
            )

        return clean_frequency

    @staticmethod
    def _validate_optional_text(
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Validate and normalize an optional text field.
        """
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        return value.strip()

    @staticmethod
    def _validate_list(
        value: list[Any],
        *,
        field_name: str,
    ) -> list[Any]:
        """
        Validate a list field.
        """
        if not isinstance(value, list):
            raise TypeError(
                f"{field_name} must be a list."
            )

        return value

    @staticmethod
    def _validate_audience(
        audience: list[str],
    ) -> list[str]:
        """
        Validate the Data Product audience.
        """
        if not isinstance(audience, list):
            raise TypeError(
                "audience must be a list."
            )

        clean_audience: list[str] = []

        for item in audience:
            if not isinstance(item, str):
                raise TypeError(
                    "Every audience item must be "
                    "a string."
                )

            clean_item = item.strip()

            if not clean_item:
                raise ValueError(
                    "Audience items cannot be empty."
                )

            clean_audience.append(clean_item)

        return clean_audience