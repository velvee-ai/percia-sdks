from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_watch_body_advanced_actions_item import (
        UpdateWatchBodyAdvancedActionsItem,
    )
    from ..models.update_watch_body_advanced_conditions_item import (
        UpdateWatchBodyAdvancedConditionsItem,
    )


T = TypeVar("T", bound="UpdateWatchBodyAdvanced")


@_attrs_define
class UpdateWatchBodyAdvanced:
    """Beta, only where recording is on (422 advanced_unavailable elsewhere): your own conditions. `conditions[]` are
    Condition objects {condition_id, kind (event|state|measurement), observable, role?: helper, while?/and_not?:
    {condition_id} or {signal: {signal, op, value}}, window_by?, window?, window_signal?, thresholds?: {..., trend,
    trend_window_s, trend_min_samples, trend_noise_floor, trend_slope}}. Example, alert if the belt stops while the
    motor is on: [{condition_id:"belt_stopped", kind:"state", observable:"the belt is not moving",
    while:{signal:{signal:"motor_running", op:"==", value:true}}}] (declare motor_running in the site's context first,
    and join the watch to that site with siteId). The source must be a Percia camera. See /docs/advanced.md.

        Attributes:
            conditions (list['UpdateWatchBodyAdvancedConditionsItem']):
            actions (Union[Unset, list['UpdateWatchBodyAdvancedActionsItem']]):
    """

    conditions: list["UpdateWatchBodyAdvancedConditionsItem"]
    actions: Union[Unset, list["UpdateWatchBodyAdvancedActionsItem"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        conditions = []
        for conditions_item_data in self.conditions:
            conditions_item = conditions_item_data.to_dict()
            conditions.append(conditions_item)

        actions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "conditions": conditions,
            }
        )
        if actions is not UNSET:
            field_dict["actions"] = actions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_watch_body_advanced_actions_item import (
            UpdateWatchBodyAdvancedActionsItem,
        )
        from ..models.update_watch_body_advanced_conditions_item import (
            UpdateWatchBodyAdvancedConditionsItem,
        )

        d = dict(src_dict)
        conditions = []
        _conditions = d.pop("conditions")
        for conditions_item_data in _conditions:
            conditions_item = UpdateWatchBodyAdvancedConditionsItem.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = UpdateWatchBodyAdvancedActionsItem.from_dict(actions_item_data)

            actions.append(actions_item)

        update_watch_body_advanced = cls(
            conditions=conditions,
            actions=actions,
        )

        return update_watch_body_advanced
