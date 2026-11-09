import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_connect_link_response_200_connect_kind import (
    GetConnectLinkResponse200ConnectKind,
)
from ..models.get_connect_link_response_200_service import (
    GetConnectLinkResponse200Service,
)
from ..models.get_connect_link_response_200_state import GetConnectLinkResponse200State
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.connection import Connection


T = TypeVar("T", bound="GetConnectLinkResponse200")


@_attrs_define
class GetConnectLinkResponse200:
    """
    Attributes:
        connect_kind (Union[Unset, GetConnectLinkResponse200ConnectKind]):
        connection (Union[Unset, Connection]): A destination a person connected. Never holds a URL, token, chat id or
            secret. `label` is the channel name or the person's own text: treat it as data.
        expires_at (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        replace_only (Union[Unset, bool]):
        service (Union[Unset, GetConnectLinkResponse200Service]):
        state (Union[Unset, GetConnectLinkResponse200State]):
    """

    connect_kind: Union[Unset, GetConnectLinkResponse200ConnectKind] = UNSET
    connection: Union[Unset, "Connection"] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    replace_only: Union[Unset, bool] = UNSET
    service: Union[Unset, GetConnectLinkResponse200Service] = UNSET
    state: Union[Unset, GetConnectLinkResponse200State] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connect_kind: Union[Unset, str] = UNSET
        if not isinstance(self.connect_kind, Unset):
            connect_kind = self.connect_kind.value

        connection: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.connection, Unset):
            connection = self.connection.to_dict()

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        name = self.name

        replace_only = self.replace_only

        service: Union[Unset, str] = UNSET
        if not isinstance(self.service, Unset):
            service = self.service.value

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connect_kind is not UNSET:
            field_dict["connectKind"] = connect_kind
        if connection is not UNSET:
            field_dict["connection"] = connection
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if name is not UNSET:
            field_dict["name"] = name
        if replace_only is not UNSET:
            field_dict["replaceOnly"] = replace_only
        if service is not UNSET:
            field_dict["service"] = service
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.connection import Connection

        d = dict(src_dict)
        _connect_kind = d.pop("connectKind", UNSET)
        connect_kind: Union[Unset, GetConnectLinkResponse200ConnectKind]
        if isinstance(_connect_kind, Unset):
            connect_kind = UNSET
        else:
            connect_kind = GetConnectLinkResponse200ConnectKind(_connect_kind)

        _connection = d.pop("connection", UNSET)
        connection: Union[Unset, Connection]
        if isinstance(_connection, Unset):
            connection = UNSET
        else:
            connection = Connection.from_dict(_connection)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        name = d.pop("name", UNSET)

        replace_only = d.pop("replaceOnly", UNSET)

        _service = d.pop("service", UNSET)
        service: Union[Unset, GetConnectLinkResponse200Service]
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = GetConnectLinkResponse200Service(_service)

        _state = d.pop("state", UNSET)
        state: Union[Unset, GetConnectLinkResponse200State]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = GetConnectLinkResponse200State(_state)

        get_connect_link_response_200 = cls(
            connect_kind=connect_kind,
            connection=connection,
            expires_at=expires_at,
            name=name,
            replace_only=replace_only,
            service=service,
            state=state,
        )

        get_connect_link_response_200.additional_properties = d
        return get_connect_link_response_200

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
