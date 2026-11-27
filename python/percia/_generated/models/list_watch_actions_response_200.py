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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_watch_actions_response_200_actions_item import (
        ListWatchActionsResponse200ActionsItem,
    )


T = TypeVar("T", bound="ListWatchActionsResponse200")


@_attrs_define
class ListWatchActionsResponse200:
    """
    Attributes:
        actions (Union[Unset, list['ListWatchActionsResponse200ActionsItem']]):
        next_cursor (Union[None, Unset, str]):
    """

    actions: Union[Unset, list["ListWatchActionsResponse200ActionsItem"]] = UNSET
    next_cursor: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)

        next_cursor: Union[None, Unset, str]
        if isinstance(self.next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if actions is not UNSET:
            field_dict["actions"] = actions
        if next_cursor is not UNSET:
            field_dict["nextCursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_watch_actions_response_200_actions_item import (
            ListWatchActionsResponse200ActionsItem,
        )

        d = dict(src_dict)
        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = ListWatchActionsResponse200ActionsItem.from_dict(actions_item_data)

            actions.append(actions_item)

        def _parse_next_cursor(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor", UNSET))

        list_watch_actions_response_200 = cls(
            actions=actions,
            next_cursor=next_cursor,
        )

        list_watch_actions_response_200.additional_properties = d
        return list_watch_actions_response_200

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
