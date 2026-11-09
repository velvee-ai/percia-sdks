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
    from ..models.agent_config_actions_item import AgentConfigActionsItem
    from ..models.agent_config_budget import AgentConfigBudget
    from ..models.agent_config_concerns_item import AgentConfigConcernsItem
    from ..models.agent_config_outputs_item import AgentConfigOutputsItem


T = TypeVar("T", bound="AgentConfig")


@_attrs_define
class AgentConfig:
    """Up to 10 concerns plus a request budget. A zone is a polygon of 3 to 12 [x, y] points, each 0..1 (fractions of the
    frame).

        Attributes:
            concerns (list['AgentConfigConcernsItem']):
            actions (Union[Unset, list['AgentConfigActionsItem']]): MCP tool calls made after an event is stored. String
                values in `arguments` may use {{event.reason}}, {{event.concern}}, {{event.at}}, {{event.confidence}},
                {{watch.name}}, {{site.name}} and {{outputs.<name>}}. A secret header is written with `value` and read back as
                `hasSecret`.
            budget (Union[Unset, AgentConfigBudget]):
            outputs (Union[Unset, list['AgentConfigOutputsItem']]): Typed values read from the event's keyframe by a
                language model and stored on the event as `outputs`.
    """

    concerns: list["AgentConfigConcernsItem"]
    actions: Union[Unset, list["AgentConfigActionsItem"]] = UNSET
    budget: Union[Unset, "AgentConfigBudget"] = UNSET
    outputs: Union[Unset, list["AgentConfigOutputsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        concerns = []
        for concerns_item_data in self.concerns:
            concerns_item = concerns_item_data.to_dict()
            concerns.append(concerns_item)

        actions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)

        budget: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.budget, Unset):
            budget = self.budget.to_dict()

        outputs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.outputs, Unset):
            outputs = []
            for outputs_item_data in self.outputs:
                outputs_item = outputs_item_data.to_dict()
                outputs.append(outputs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "concerns": concerns,
            }
        )
        if actions is not UNSET:
            field_dict["actions"] = actions
        if budget is not UNSET:
            field_dict["budget"] = budget
        if outputs is not UNSET:
            field_dict["outputs"] = outputs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_actions_item import AgentConfigActionsItem
        from ..models.agent_config_budget import AgentConfigBudget
        from ..models.agent_config_concerns_item import AgentConfigConcernsItem
        from ..models.agent_config_outputs_item import AgentConfigOutputsItem

        d = dict(src_dict)
        concerns = []
        _concerns = d.pop("concerns")
        for concerns_item_data in _concerns:
            concerns_item = AgentConfigConcernsItem.from_dict(concerns_item_data)

            concerns.append(concerns_item)

        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = AgentConfigActionsItem.from_dict(actions_item_data)

            actions.append(actions_item)

        _budget = d.pop("budget", UNSET)
        budget: Union[Unset, AgentConfigBudget]
        if isinstance(_budget, Unset):
            budget = UNSET
        else:
            budget = AgentConfigBudget.from_dict(_budget)

        outputs = []
        _outputs = d.pop("outputs", UNSET)
        for outputs_item_data in _outputs or []:
            outputs_item = AgentConfigOutputsItem.from_dict(outputs_item_data)

            outputs.append(outputs_item)

        agent_config = cls(
            concerns=concerns,
            actions=actions,
            budget=budget,
            outputs=outputs,
        )

        agent_config.additional_properties = d
        return agent_config

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
