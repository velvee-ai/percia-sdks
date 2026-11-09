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

from ..models.update_integration_response_200_service import (
    UpdateIntegrationResponse200Service,
)
from ..models.update_integration_response_200_status import (
    UpdateIntegrationResponse200Status,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateIntegrationResponse200")


@_attrs_define
class UpdateIntegrationResponse200:
    """
    Attributes:
        applied (Union[Unset, int]):
        created_at (Union[Unset, datetime.datetime]):
        default (Union[Unset, bool]): True = attached to every new watch you create, by Percia itself: do not ask about
            it and do not attach it again.
        id (Union[Unset, str]):
        label (Union[Unset, str]):
        last_delivered_at (Union[None, Unset, datetime.datetime]):
        last_error (Union[None, Unset, str]): Stable code: why it broke, or why the last delivery failed for good.
        service (Union[Unset, UpdateIntegrationResponse200Service]):
        status (Union[Unset, UpdateIntegrationResponse200Status]): broken = the service refused the credential: no more
            deliveries, connect it again.
    """

    applied: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    default: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    last_delivered_at: Union[None, Unset, datetime.datetime] = UNSET
    last_error: Union[None, Unset, str] = UNSET
    service: Union[Unset, UpdateIntegrationResponse200Service] = UNSET
    status: Union[Unset, UpdateIntegrationResponse200Status] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        applied = self.applied

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        default = self.default

        id = self.id

        label = self.label

        last_delivered_at: Union[None, Unset, str]
        if isinstance(self.last_delivered_at, Unset):
            last_delivered_at = UNSET
        elif isinstance(self.last_delivered_at, datetime.datetime):
            last_delivered_at = self.last_delivered_at.isoformat()
        else:
            last_delivered_at = self.last_delivered_at

        last_error: Union[None, Unset, str]
        if isinstance(self.last_error, Unset):
            last_error = UNSET
        else:
            last_error = self.last_error

        service: Union[Unset, str] = UNSET
        if not isinstance(self.service, Unset):
            service = self.service.value

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if applied is not UNSET:
            field_dict["applied"] = applied
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if default is not UNSET:
            field_dict["default"] = default
        if id is not UNSET:
            field_dict["id"] = id
        if label is not UNSET:
            field_dict["label"] = label
        if last_delivered_at is not UNSET:
            field_dict["lastDeliveredAt"] = last_delivered_at
        if last_error is not UNSET:
            field_dict["lastError"] = last_error
        if service is not UNSET:
            field_dict["service"] = service
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        applied = d.pop("applied", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        default = d.pop("default", UNSET)

        id = d.pop("id", UNSET)

        label = d.pop("label", UNSET)

        def _parse_last_delivered_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_delivered_at_type_0 = isoparse(data)

                return last_delivered_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_delivered_at = _parse_last_delivered_at(d.pop("lastDeliveredAt", UNSET))

        def _parse_last_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_error = _parse_last_error(d.pop("lastError", UNSET))

        _service = d.pop("service", UNSET)
        service: Union[Unset, UpdateIntegrationResponse200Service]
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = UpdateIntegrationResponse200Service(_service)

        _status = d.pop("status", UNSET)
        status: Union[Unset, UpdateIntegrationResponse200Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = UpdateIntegrationResponse200Status(_status)

        update_integration_response_200 = cls(
            applied=applied,
            created_at=created_at,
            default=default,
            id=id,
            label=label,
            last_delivered_at=last_delivered_at,
            last_error=last_error,
            service=service,
            status=status,
        )

        update_integration_response_200.additional_properties = d
        return update_integration_response_200

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
