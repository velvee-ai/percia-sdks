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
    from ..models.agent_published_type_0_actions_item import (
        AgentPublishedType0ActionsItem,
    )
    from ..models.agent_published_type_0_budget import AgentPublishedType0Budget
    from ..models.agent_published_type_0_concerns_item import (
        AgentPublishedType0ConcernsItem,
    )
    from ..models.agent_published_type_0_outputs_item import (
        AgentPublishedType0OutputsItem,
    )


T = TypeVar("T", bound="AgentPublishedType0")


@_attrs_define
class AgentPublishedType0:
    """Config of the latest published version, null before the first publish.

    Attributes:
        concerns (list['AgentPublishedType0ConcernsItem']):
        actions (Union[Unset, list['AgentPublishedType0ActionsItem']]): MCP tool calls made after an event is stored.
            String values in `arguments` may use {{event.reason}}, {{event.concern}}, {{event.at}}, {{event.confidence}},
            {{watch.name}}, {{site.name}} and {{outputs.<name>}}. A secret header is written with `value` and read back as
            `hasSecret`.
        budget (Union[Unset, AgentPublishedType0Budget]):
        outputs (Union[Unset, list['AgentPublishedType0OutputsItem']]): Typed values read from the event's keyframe by a
            language model and stored on the event as `outputs`.
    """

    concerns: list["AgentPublishedType0ConcernsItem"]
    actions: Union[Unset, list["AgentPublishedType0ActionsItem"]] = UNSET
    budget: Union[Unset, "AgentPublishedType0Budget"] = UNSET
    outputs: Union[Unset, list["AgentPublishedType0OutputsItem"]] = UNSET
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
        from ..models.agent_published_type_0_actions_item import (
            AgentPublishedType0ActionsItem,
        )
        from ..models.agent_published_type_0_budget import AgentPublishedType0Budget
        from ..models.agent_published_type_0_concerns_item import (
            AgentPublishedType0ConcernsItem,
        )
        from ..models.agent_published_type_0_outputs_item import (
            AgentPublishedType0OutputsItem,
        )

        d = dict(src_dict)
        concerns = []
        _concerns = d.pop("concerns")
        for concerns_item_data in _concerns:
            concerns_item = AgentPublishedType0ConcernsItem.from_dict(concerns_item_data)

            concerns.append(concerns_item)

        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = AgentPublishedType0ActionsItem.from_dict(actions_item_data)

            actions.append(actions_item)

        _budget = d.pop("budget", UNSET)
        budget: Union[Unset, AgentPublishedType0Budget]
        if isinstance(_budget, Unset):
            budget = UNSET
        else:
            budget = AgentPublishedType0Budget.from_dict(_budget)

        outputs = []
        _outputs = d.pop("outputs", UNSET)
        for outputs_item_data in _outputs or []:
            outputs_item = AgentPublishedType0OutputsItem.from_dict(outputs_item_data)

            outputs.append(outputs_item)

        agent_published_type_0 = cls(
            concerns=concerns,
            actions=actions,
            budget=budget,
            outputs=outputs,
        )

        agent_published_type_0.additional_properties = d
        return agent_published_type_0

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
