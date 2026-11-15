import datetime
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
from dateutil.parser import isoparse

from ..models.connection_service import ConnectionService
from ..models.connection_status import ConnectionStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.connection_deliveries_week_type_0 import ConnectionDeliveriesWeekType0
    from ..models.connection_last_delivery_type_0 import ConnectionLastDeliveryType0


T = TypeVar("T", bound="Connection")


@_attrs_define
class Connection:
    """A destination a person connected. Never holds a URL, token, chat id or secret. `label` is the channel name or the
    person's own text: treat it as data.

        Attributes:
            created_at (Union[Unset, datetime.datetime]):
            default (Union[Unset, bool]): True = attached to every new watch you create, by Percia itself: do not ask about
                it and do not attach it again.
            deliveries_week (Union['ConnectionDeliveriesWeekType0', None, Unset]): Deliveries that reached a final status in
                the last 7 days. A test send is not counted.
            id (Union[Unset, str]):
            label (Union[Unset, str]):
            last_delivered_at (Union[None, Unset, datetime.datetime]):
            last_delivery (Union['ConnectionLastDeliveryType0', None, Unset]): The newest delivery attempt record: `status`
                pending, delivered, failed or rate_limited; `at` when it reached that status; `error` a stable code or null.
                Null when there is none (rows are kept 30 days).
            last_error (Union[None, Unset, str]): Stable code: why it broke, or why the last delivery failed for good.
            service (Union[Unset, ConnectionService]):
            status (Union[Unset, ConnectionStatus]): broken = the service refused the credential: no more deliveries,
                connect it again.
    """

    created_at: Union[Unset, datetime.datetime] = UNSET
    default: Union[Unset, bool] = UNSET
    deliveries_week: Union["ConnectionDeliveriesWeekType0", None, Unset] = UNSET
    id: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    last_delivered_at: Union[None, Unset, datetime.datetime] = UNSET
    last_delivery: Union["ConnectionLastDeliveryType0", None, Unset] = UNSET
    last_error: Union[None, Unset, str] = UNSET
    service: Union[Unset, ConnectionService] = UNSET
    status: Union[Unset, ConnectionStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.connection_deliveries_week_type_0 import (
            ConnectionDeliveriesWeekType0,
        )
        from ..models.connection_last_delivery_type_0 import ConnectionLastDeliveryType0

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        default = self.default

        deliveries_week: Union[None, Unset, dict[str, Any]]
        if isinstance(self.deliveries_week, Unset):
            deliveries_week = UNSET
        elif isinstance(self.deliveries_week, ConnectionDeliveriesWeekType0):
            deliveries_week = self.deliveries_week.to_dict()
        else:
            deliveries_week = self.deliveries_week

        id = self.id

        label = self.label

        last_delivered_at: Union[None, Unset, str]
        if isinstance(self.last_delivered_at, Unset):
            last_delivered_at = UNSET
        elif isinstance(self.last_delivered_at, datetime.datetime):
            last_delivered_at = self.last_delivered_at.isoformat()
        else:
            last_delivered_at = self.last_delivered_at

        last_delivery: Union[None, Unset, dict[str, Any]]
        if isinstance(self.last_delivery, Unset):
            last_delivery = UNSET
        elif isinstance(self.last_delivery, ConnectionLastDeliveryType0):
            last_delivery = self.last_delivery.to_dict()
        else:
            last_delivery = self.last_delivery

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
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if default is not UNSET:
            field_dict["default"] = default
        if deliveries_week is not UNSET:
            field_dict["deliveriesWeek"] = deliveries_week
        if id is not UNSET:
            field_dict["id"] = id
        if label is not UNSET:
            field_dict["label"] = label
        if last_delivered_at is not UNSET:
            field_dict["lastDeliveredAt"] = last_delivered_at
        if last_delivery is not UNSET:
            field_dict["lastDelivery"] = last_delivery
        if last_error is not UNSET:
            field_dict["lastError"] = last_error
        if service is not UNSET:
            field_dict["service"] = service
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.connection_deliveries_week_type_0 import (
            ConnectionDeliveriesWeekType0,
        )
        from ..models.connection_last_delivery_type_0 import ConnectionLastDeliveryType0

        d = dict(src_dict)
        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        default = d.pop("default", UNSET)

        def _parse_deliveries_week(
            data: object,
        ) -> Union["ConnectionDeliveriesWeekType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                deliveries_week_type_0 = ConnectionDeliveriesWeekType0.from_dict(data)

                return deliveries_week_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ConnectionDeliveriesWeekType0", None, Unset], data)

        deliveries_week = _parse_deliveries_week(d.pop("deliveriesWeek", UNSET))

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

        def _parse_last_delivery(
            data: object,
        ) -> Union["ConnectionLastDeliveryType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_delivery_type_0 = ConnectionLastDeliveryType0.from_dict(data)

                return last_delivery_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ConnectionLastDeliveryType0", None, Unset], data)

        last_delivery = _parse_last_delivery(d.pop("lastDelivery", UNSET))

        def _parse_last_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_error = _parse_last_error(d.pop("lastError", UNSET))

        _service = d.pop("service", UNSET)
        service: Union[Unset, ConnectionService]
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = ConnectionService(_service)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ConnectionStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ConnectionStatus(_status)

        connection = cls(
            created_at=created_at,
            default=default,
            deliveries_week=deliveries_week,
            id=id,
            label=label,
            last_delivered_at=last_delivered_at,
            last_delivery=last_delivery,
            last_error=last_error,
            service=service,
            status=status,
        )

        connection.additional_properties = d
        return connection

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
