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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_watch_actions_response_200_actions_item_action import (
        ListWatchActionsResponse200ActionsItemAction,
    )


T = TypeVar("T", bound="ListWatchActionsResponse200ActionsItem")


@_attrs_define
class ListWatchActionsResponse200ActionsItem:
    """
    Attributes:
        action (Union[Unset, ListWatchActionsResponse200ActionsItemAction]):
        created_at (Union[Unset, datetime.datetime]):
        id (Union[Unset, str]):
        kind (Union[Unset, str]):
        t (Union[Unset, float]):
    """

    action: Union[Unset, "ListWatchActionsResponse200ActionsItemAction"] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET
    kind: Union[Unset, str] = UNSET
    t: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.action, Unset):
            action = self.action.to_dict()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        id = self.id

        kind = self.kind

        t = self.t

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if kind is not UNSET:
            field_dict["kind"] = kind
        if t is not UNSET:
            field_dict["t"] = t

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_watch_actions_response_200_actions_item_action import (
            ListWatchActionsResponse200ActionsItemAction,
        )

        d = dict(src_dict)
        _action = d.pop("action", UNSET)
        action: Union[Unset, ListWatchActionsResponse200ActionsItemAction]
        if isinstance(_action, Unset):
            action = UNSET
        else:
            action = ListWatchActionsResponse200ActionsItemAction.from_dict(_action)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        id = d.pop("id", UNSET)

        kind = d.pop("kind", UNSET)

        t = d.pop("t", UNSET)

        list_watch_actions_response_200_actions_item = cls(
            action=action,
            created_at=created_at,
            id=id,
            kind=kind,
            t=t,
        )

        list_watch_actions_response_200_actions_item.additional_properties = d
        return list_watch_actions_response_200_actions_item

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
