from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.integration_result_service import IntegrationResultService
from ..models.integration_result_status import IntegrationResultStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegrationResult")


@_attrs_define
class IntegrationResult:
    """
    Attributes:
        attempts (int):
        connection_id (str):
        service (IntegrationResultService):
        status (IntegrationResultStatus): rate_limited: the connection's own hourly send limit (SMS, WhatsApp) was used
            up; the connection stays active.
        error (Union[Unset, str]): Stable code, when the last attempt failed.
    """

    attempts: int
    connection_id: str
    service: IntegrationResultService
    status: IntegrationResultStatus
    error: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempts = self.attempts

        connection_id = self.connection_id

        service = self.service.value

        status = self.status.value

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempts": attempts,
                "connectionId": connection_id,
                "service": service,
                "status": status,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attempts = d.pop("attempts")

        connection_id = d.pop("connectionId")

        service = IntegrationResultService(d.pop("service"))

        status = IntegrationResultStatus(d.pop("status"))

        error = d.pop("error", UNSET)

        integration_result = cls(
            attempts=attempts,
            connection_id=connection_id,
            service=service,
            status=status,
            error=error,
        )

        integration_result.additional_properties = d
        return integration_result

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
