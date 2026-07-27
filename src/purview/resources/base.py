from __future__ import annotations

from typing import Any, Generic, TypeVar
from uuid import UUID

from purview.http_client import PurviewHttpClient


ModelType = TypeVar("ModelType")


class BaseResourceClient(Generic[ModelType]):
    """
    Base client for Microsoft Purview Unified Catalog resources.

    This class provides the collection and item operations shared by
    Purview resources that follow these documented endpoint patterns:

        GET    /{resource}
        GET    /{resource}/{resource_id}
        POST   /{resource}
        PUT    /{resource}/{resource_id}
        DELETE /{resource}/{resource_id}

    Subclasses must define:

        RESOURCE_PATH = "resourceName"
        MODEL = ModelClass

    Resource-specific clients remain responsible for validating their
    documented request fields and constructing the correct request body.
    """

    RESOURCE_PATH: str = ""
    MODEL: type[ModelType] | None = None

    def __init__(
        self,
        http_client: PurviewHttpClient,
    ) -> None:
        self.http = http_client

    @property
    def resource_path(self) -> str:
        """
        Return the normalized collection path for this resource.
        """
        path = self.RESOURCE_PATH.strip().strip("/")

        if not path:
            raise ValueError(
                f"{self.__class__.__name__}.RESOURCE_PATH "
                "must be defined."
            )

        return f"/{path}"

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
    def _validate_id(
        cls,
        resource_id: str,
        *,
        field_name: str = "resource_id",
    ) -> str:
        """
        Validate and normalize a non-empty resource identifier.

        Use _validate_uuid() in a resource client when the corresponding
        Purview API parameter is documented as a UUID.
        """
        return cls._validate_text(
            resource_id,
            field_name=field_name,
        )

    @classmethod
    def _validate_uuid(
        cls,
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Validate and normalize a UUID string.
        """
        clean_value = cls._validate_text(
            value,
            field_name=field_name,
        )

        try:
            return str(UUID(clean_value))
        except ValueError as error:
            raise ValueError(
                f"{field_name} must be a valid UUID."
            ) from error

    @staticmethod
    def _validate_payload(
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Validate a non-empty JSON object request body.
        """
        if not isinstance(payload, dict):
            raise TypeError(
                "payload must be a dictionary."
            )

        if not payload:
            raise ValueError(
                "payload cannot be empty."
            )

        return payload

    def _item_path(
        self,
        resource_id: str,
        *,
        field_name: str = "resource_id",
    ) -> str:
        """
        Build the documented item path /{resource}/{resource_id}.
        """
        clean_id = self._validate_id(
            resource_id,
            field_name=field_name,
        )

        return f"{self.resource_path}/{clean_id}"

    def _subresource_path(
        self,
        resource_id: str,
        subresource: str,
        *,
        field_name: str = "resource_id",
    ) -> str:
        """
        Build a nested path such as
        /{resource}/{resource_id}/relationships.
        """
        clean_subresource = self._validate_text(
            subresource,
            field_name="subresource",
        ).strip("/")

        if not clean_subresource:
            raise ValueError(
                "subresource cannot be empty."
            )

        return (
            f"{self._item_path(resource_id, field_name=field_name)}/"
            f"{clean_subresource}"
        )

    def _to_model(
        self,
        data: dict[str, Any],
    ) -> ModelType:
        """
        Convert one Purview response object into the configured model.
        """
        if not isinstance(data, dict):
            raise TypeError(
                "Model data must be a dictionary."
            )

        if self.MODEL is None:
            raise ValueError(
                f"{self.__class__.__name__}.MODEL "
                "must be defined."
            )

        from_dict = getattr(
            self.MODEL,
            "from_dict",
            None,
        )

        if not callable(from_dict):
            raise TypeError(
                f"{self.MODEL.__name__} must define "
                "a callable from_dict() method."
            )

        return from_dict(data)

    def _to_model_list(
        self,
        response: dict[str, Any],
        *,
        collection_key: str = "value",
    ) -> list[ModelType]:
        """
        Convert a documented response collection into model objects.

        Most Unified Catalog list endpoints used by resource clients
        return their records under ``value``. A caller may provide a
        different documented key for a specific endpoint.
        """
        if not isinstance(response, dict):
            raise TypeError(
                "response must be a dictionary."
            )

        clean_collection_key = self._validate_text(
            collection_key,
            field_name="collection_key",
        )

        if clean_collection_key not in response:
            raise KeyError(
                "Expected response to contain "
                f"{clean_collection_key!r}."
            )

        items = response[clean_collection_key]

        if not isinstance(items, list):
            raise TypeError(
                f"Expected response[{clean_collection_key!r}] "
                "to be a list."
            )

        models: list[ModelType] = []

        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise TypeError(
                    f"Expected response[{clean_collection_key!r}]"
                    f"[{index}] to be a dictionary."
                )

            models.append(
                self._to_model(item)
            )

        return models

    def list_raw(
        self,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send GET /{resource} and return the complete response.
        """
        return self.http.get(
            self.resource_path,
            params=params,
        )

    def list(
        self,
        *,
        params: dict[str, Any] | None = None,
    ) -> list[ModelType]:
        """
        Send GET /{resource} and return model objects from ``value``.
        """
        response = self.list_raw(
            params=params,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected list response to be a dictionary."
            )

        return self._to_model_list(
            response,
            collection_key="value",
        )

    def get_raw(
        self,
        resource_id: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send GET /{resource}/{resource_id} and return the response.
        """
        return self.http.get(
            self._item_path(resource_id),
            params=params,
        )

    def get(
        self,
        resource_id: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> ModelType:
        """
        Retrieve one resource and return its model object.
        """
        response = self.get_raw(
            resource_id,
            params=params,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected get response to be a dictionary."
            )

        return self._to_model(response)

    def create_raw(
        self,
        payload: dict[str, Any],
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send POST /{resource} and return the complete response.
        """
        clean_payload = self._validate_payload(payload)

        return self.http.post(
            self.resource_path,
            params=params,
            json=clean_payload,
        )

    def create(
        self,
        payload: dict[str, Any],
        *,
        params: dict[str, Any] | None = None,
    ) -> ModelType:
        """
        Create one resource and return its model object.
        """
        response = self.create_raw(
            payload,
            params=params,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected create response to be a dictionary."
            )

        return self._to_model(response)

    def put_raw(
        self,
        resource_id: str,
        payload: dict[str, Any],
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send PUT /{resource}/{resource_id} and return the response.
        """
        clean_payload = self._validate_payload(payload)

        return self.http.put(
            self._item_path(resource_id),
            params=params,
            json=clean_payload,
        )

    def put(
        self,
        resource_id: str,
        payload: dict[str, Any],
        *,
        params: dict[str, Any] | None = None,
    ) -> ModelType:
        """
        Update one resource with PUT and return its model object.
        """
        response = self.put_raw(
            resource_id,
            payload,
            params=params,
        )

        if not isinstance(response, dict):
            raise TypeError(
                "Expected PUT response to be a dictionary."
            )

        return self._to_model(response)

    def delete_raw(
        self,
        resource_id: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send DELETE /{resource}/{resource_id}.
        """
        return self.http.delete(
            self._item_path(resource_id),
            params=params,
        )

    def delete(
        self,
        resource_id: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Delete one resource and return the raw API result.
        """
        return self.delete_raw(
            resource_id,
            params=params,
        )