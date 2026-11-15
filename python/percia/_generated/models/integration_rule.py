from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.integration_rule_service import IntegrationRuleService
from ..models.integration_rule_status import IntegrationRuleStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_rule_last_delivery_type_0 import (
        IntegrationRuleLastDeliveryType0,
    )


T = TypeVar("T", bound="IntegrationRule")


@_attrs_define
class IntegrationRule:
    """
    Attributes:
        connection_id (Union[Unset, str]):
        label (Union[Unset, str]):
        last_delivery (Union['IntegrationRuleLastDeliveryType0', None, Unset]): The newest delivery attempt record:
            `status` pending, delivered, failed or rate_limited; `at` when it reached that status; `error` a stable code or
            null. Null when there is none (rows are kept 30 days).
        on (Union[Unset, str]): "*" or a concern id of the watch.
        service (Union[Unset, IntegrationRuleService]):
        status (Union[Unset, IntegrationRuleStatus]):
    """

    connection_id: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    last_delivery: Union["IntegrationRuleLastDeliveryType0", None, Unset] = UNSET
    on: Union[Unset, str] = UNSET
    service: Union[Unset, IntegrationRuleService] = UNSET
    status: Union[Unset, IntegrationRuleStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.integration_rule_last_delivery_type_0 import (
            IntegrationRuleLastDeliveryType0,
        )

        connection_id = self.connection_id

        label = self.label

        last_delivery: Union[None, Unset, dict[str, Any]]
        if isinstance(self.last_delivery, Unset):
            last_delivery = UNSET
        elif isinstance(self.last_delivery, IntegrationRuleLastDeliveryType0):
            last_delivery = self.last_delivery.to_dict()
        else:
            last_delivery = self.last_delivery

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
        if last_delivery is not UNSET:
            field_dict["lastDelivery"] = last_delivery
        if on is not UNSET:
            field_dict["on"] = on
        if service is not UNSET:
            field_dict["service"] = service
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_rule_last_delivery_type_0 import (
            IntegrationRuleLastDeliveryType0,
        )

        d = dict(src_dict)
        connection_id = d.pop("connectionId", UNSET)

        label = d.pop("label", UNSET)

        def _parse_last_delivery(
            data: object,
        ) -> Union["IntegrationRuleLastDeliveryType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_delivery_type_0 = IntegrationRuleLastDeliveryType0.from_dict(data)

                return last_delivery_type_0
            except:  # noqa: E722
                pass
            return cast(Union["IntegrationRuleLastDeliveryType0", None, Unset], data)

        last_delivery = _parse_last_delivery(d.pop("lastDelivery", UNSET))

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
            last_delivery=last_delivery,
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
