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

from ..models.watch_advanced_state import WatchAdvancedState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.watch_advanced_actions_item import WatchAdvancedActionsItem
    from ..models.watch_advanced_conditions_item import WatchAdvancedConditionsItem
    from ..models.watch_advanced_context_requests_item import (
        WatchAdvancedContextRequestsItem,
    )


T = TypeVar("T", bound="WatchAdvanced")


@_attrs_define
class WatchAdvanced:
    """Only on a watch made with `advanced` (Percia engine). `conditions` and `actions` as you sent them; `contextRequests`
    are what the engine asked you to supply (each has `how_to_supply`, a SiteContext path to PUT), `[]` when none or not
    yet known; `state` is `pending` until the engine reported them; `siteRev` is the revision of the site's context it
    runs on.

        Attributes:
            actions (Union[Unset, list['WatchAdvancedActionsItem']]):
            conditions (Union[Unset, list['WatchAdvancedConditionsItem']]):
            context_requests (Union[Unset, list['WatchAdvancedContextRequestsItem']]):
            site_rev (Union[None, Unset, int]):
            state (Union[Unset, WatchAdvancedState]):
    """

    actions: Union[Unset, list["WatchAdvancedActionsItem"]] = UNSET
    conditions: Union[Unset, list["WatchAdvancedConditionsItem"]] = UNSET
    context_requests: Union[Unset, list["WatchAdvancedContextRequestsItem"]] = UNSET
    site_rev: Union[None, Unset, int] = UNSET
    state: Union[Unset, WatchAdvancedState] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)

        conditions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = []
            for conditions_item_data in self.conditions:
                conditions_item = conditions_item_data.to_dict()
                conditions.append(conditions_item)

        context_requests: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.context_requests, Unset):
            context_requests = []
            for context_requests_item_data in self.context_requests:
                context_requests_item = context_requests_item_data.to_dict()
                context_requests.append(context_requests_item)

        site_rev: Union[None, Unset, int]
        if isinstance(self.site_rev, Unset):
            site_rev = UNSET
        else:
            site_rev = self.site_rev

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if actions is not UNSET:
            field_dict["actions"] = actions
        if conditions is not UNSET:
            field_dict["conditions"] = conditions
        if context_requests is not UNSET:
            field_dict["contextRequests"] = context_requests
        if site_rev is not UNSET:
            field_dict["siteRev"] = site_rev
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.watch_advanced_actions_item import WatchAdvancedActionsItem
        from ..models.watch_advanced_conditions_item import WatchAdvancedConditionsItem
        from ..models.watch_advanced_context_requests_item import (
            WatchAdvancedContextRequestsItem,
        )

        d = dict(src_dict)
        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = WatchAdvancedActionsItem.from_dict(actions_item_data)

            actions.append(actions_item)

        conditions = []
        _conditions = d.pop("conditions", UNSET)
        for conditions_item_data in _conditions or []:
            conditions_item = WatchAdvancedConditionsItem.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        context_requests = []
        _context_requests = d.pop("contextRequests", UNSET)
        for context_requests_item_data in _context_requests or []:
            context_requests_item = WatchAdvancedContextRequestsItem.from_dict(context_requests_item_data)

            context_requests.append(context_requests_item)

        def _parse_site_rev(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        site_rev = _parse_site_rev(d.pop("siteRev", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, WatchAdvancedState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = WatchAdvancedState(_state)

        watch_advanced = cls(
            actions=actions,
            conditions=conditions,
            context_requests=context_requests,
            site_rev=site_rev,
            state=state,
        )

        watch_advanced.additional_properties = d
        return watch_advanced

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
