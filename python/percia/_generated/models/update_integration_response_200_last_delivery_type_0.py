import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.update_integration_response_200_last_delivery_type_0_status import (
    UpdateIntegrationResponse200LastDeliveryType0Status,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateIntegrationResponse200LastDeliveryType0")


@_attrs_define
class UpdateIntegrationResponse200LastDeliveryType0:
    """The newest delivery attempt record: `status` pending, delivered, failed or rate_limited; `at` when it reached that
    status; `error` a stable code or null. Null when there is none (rows are kept 30 days).

        Attributes:
            at (Union[Unset, datetime.datetime]):
            error (Union[None, Unset, str]):
            status (Union[Unset, UpdateIntegrationResponse200LastDeliveryType0Status]):
    """

    at: Union[Unset, datetime.datetime] = UNSET
    error: Union[None, Unset, str] = UNSET
    status: Union[Unset, UpdateIntegrationResponse200LastDeliveryType0Status] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at: Union[Unset, str] = UNSET
        if not isinstance(self.at, Unset):
            at = self.at.isoformat()

        error: Union[None, Unset, str]
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if at is not UNSET:
            field_dict["at"] = at
        if error is not UNSET:
            field_dict["error"] = error
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _at = d.pop("at", UNSET)
        at: Union[Unset, datetime.datetime]
        if isinstance(_at, Unset):
            at = UNSET
        else:
            at = isoparse(_at)

        def _parse_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error = _parse_error(d.pop("error", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, UpdateIntegrationResponse200LastDeliveryType0Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = UpdateIntegrationResponse200LastDeliveryType0Status(_status)

        update_integration_response_200_last_delivery_type_0 = cls(
            at=at,
            error=error,
            status=status,
        )

        update_integration_response_200_last_delivery_type_0.additional_properties = d
        return update_integration_response_200_last_delivery_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
