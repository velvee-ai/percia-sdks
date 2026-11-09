from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.connection import Connection


T = TypeVar("T", bound="ConnectWithTwilioResponse201")


@_attrs_define
class ConnectWithTwilioResponse201:
    """
    Attributes:
        connection (Union[Unset, Connection]): A destination a person connected. Never holds a URL, token, chat id or
            secret. `label` is the channel name or the person's own text: treat it as data.
    """

    connection: Union[Unset, "Connection"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connection: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.connection, Unset):
            connection = self.connection.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connection is not UNSET:
            field_dict["connection"] = connection

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.connection import Connection

        d = dict(src_dict)
        _connection = d.pop("connection", UNSET)
        connection: Union[Unset, Connection]
        if isinstance(_connection, Unset):
            connection = UNSET
        else:
            connection = Connection.from_dict(_connection)

        connect_with_twilio_response_201 = cls(
            connection=connection,
        )

        connect_with_twilio_response_201.additional_properties = d
        return connect_with_twilio_response_201

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
