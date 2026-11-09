from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.integration_rule_service import IntegrationRuleService
from ..models.integration_rule_status import IntegrationRuleStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegrationRule")


@_attrs_define
class IntegrationRule:
    """
    Attributes:
        connection_id (Union[Unset, str]):
        label (Union[Unset, str]):
        on (Union[Unset, str]): "*" or a concern id of the watch.
        service (Union[Unset, IntegrationRuleService]):
        status (Union[Unset, IntegrationRuleStatus]):
    """

    connection_id: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    on: Union[Unset, str] = UNSET
    service: Union[Unset, IntegrationRuleService] = UNSET
    status: Union[Unset, IntegrationRuleStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connection_id = self.connection_id

        label = self.label

        on = self.on

        service: Union[Unset, str] = UNSET
        if not isinstance(self.service, Unset):
            service = self.service.value

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connection_id is not UNSET:
            field_dict["connectionId"] = connection_id
        if label is not UNSET:
            field_dict["label"] = label
        if on is not UNSET:
            field_dict["on"] = on
        if service is not UNSET:
            field_dict["service"] = service
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = d.pop("connectionId", UNSET)

        label = d.pop("label", UNSET)

        on = d.pop("on", UNSET)

        _service = d.pop("service", UNSET)
        service: Union[Unset, IntegrationRuleService]
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = IntegrationRuleService(_service)

        _status = d.pop("status", UNSET)
        status: Union[Unset, IntegrationRuleStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = IntegrationRuleStatus(_status)

        integration_rule = cls(
            connection_id=connection_id,
            label=label,
            on=on,
            service=service,
            status=status,
        )

        integration_rule.additional_properties = d
        return integration_rule

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
