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
    from ..models.create_agent_body_config_actions_item import (
        CreateAgentBodyConfigActionsItem,
    )
    from ..models.create_agent_body_config_budget import CreateAgentBodyConfigBudget
    from ..models.create_agent_body_config_concerns_item import (
        CreateAgentBodyConfigConcernsItem,
    )
    from ..models.create_agent_body_config_outputs_item import (
        CreateAgentBodyConfigOutputsItem,
    )


T = TypeVar("T", bound="CreateAgentBodyConfig")


@_attrs_define
class CreateAgentBodyConfig:
    """
    Attributes:
        concerns (list['CreateAgentBodyConfigConcernsItem']):
        actions (Union[Unset, list['CreateAgentBodyConfigActionsItem']]):
        budget (Union[Unset, CreateAgentBodyConfigBudget]):
        outputs (Union[Unset, list['CreateAgentBodyConfigOutputsItem']]):
    """

    concerns: list["CreateAgentBodyConfigConcernsItem"]
    actions: Union[Unset, list["CreateAgentBodyConfigActionsItem"]] = UNSET
    budget: Union[Unset, "CreateAgentBodyConfigBudget"] = UNSET
    outputs: Union[Unset, list["CreateAgentBodyConfigOutputsItem"]] = UNSET

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
        from ..models.create_agent_body_config_actions_item import (
            CreateAgentBodyConfigActionsItem,
        )
        from ..models.create_agent_body_config_budget import CreateAgentBodyConfigBudget
        from ..models.create_agent_body_config_concerns_item import (
            CreateAgentBodyConfigConcernsItem,
        )
        from ..models.create_agent_body_config_outputs_item import (
            CreateAgentBodyConfigOutputsItem,
        )

        d = dict(src_dict)
        concerns = []
        _concerns = d.pop("concerns")
        for concerns_item_data in _concerns:
            concerns_item = CreateAgentBodyConfigConcernsItem.from_dict(concerns_item_data)

            concerns.append(concerns_item)

        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = CreateAgentBodyConfigActionsItem.from_dict(actions_item_data)

            actions.append(actions_item)

        _budget = d.pop("budget", UNSET)
        budget: Union[Unset, CreateAgentBodyConfigBudget]
        if isinstance(_budget, Unset):
            budget = UNSET
        else:
            budget = CreateAgentBodyConfigBudget.from_dict(_budget)

        outputs = []
        _outputs = d.pop("outputs", UNSET)
        for outputs_item_data in _outputs or []:
            outputs_item = CreateAgentBodyConfigOutputsItem.from_dict(outputs_item_data)

            outputs.append(outputs_item)

        create_agent_body_config = cls(
            concerns=concerns,
            actions=actions,
            budget=budget,
            outputs=outputs,
        )

        return create_agent_body_config
