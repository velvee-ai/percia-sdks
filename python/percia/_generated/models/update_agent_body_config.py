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
    from ..models.update_agent_body_config_actions_item import (
        UpdateAgentBodyConfigActionsItem,
    )
    from ..models.update_agent_body_config_budget import UpdateAgentBodyConfigBudget
    from ..models.update_agent_body_config_concerns_item import (
        UpdateAgentBodyConfigConcernsItem,
    )
    from ..models.update_agent_body_config_outputs_item import (
        UpdateAgentBodyConfigOutputsItem,
    )


T = TypeVar("T", bound="UpdateAgentBodyConfig")


@_attrs_define
class UpdateAgentBodyConfig:
    """
    Attributes:
        concerns (list['UpdateAgentBodyConfigConcernsItem']):
        actions (Union[Unset, list['UpdateAgentBodyConfigActionsItem']]):
        budget (Union[Unset, UpdateAgentBodyConfigBudget]):
        outputs (Union[Unset, list['UpdateAgentBodyConfigOutputsItem']]):
    """

    concerns: list["UpdateAgentBodyConfigConcernsItem"]
    actions: Union[Unset, list["UpdateAgentBodyConfigActionsItem"]] = UNSET
    budget: Union[Unset, "UpdateAgentBodyConfigBudget"] = UNSET
    outputs: Union[Unset, list["UpdateAgentBodyConfigOutputsItem"]] = UNSET

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
        from ..models.update_agent_body_config_actions_item import (
            UpdateAgentBodyConfigActionsItem,
        )
        from ..models.update_agent_body_config_budget import UpdateAgentBodyConfigBudget
        from ..models.update_agent_body_config_concerns_item import (
            UpdateAgentBodyConfigConcernsItem,
        )
        from ..models.update_agent_body_config_outputs_item import (
            UpdateAgentBodyConfigOutputsItem,
        )

        d = dict(src_dict)
        concerns = []
        _concerns = d.pop("concerns")
        for concerns_item_data in _concerns:
            concerns_item = UpdateAgentBodyConfigConcernsItem.from_dict(concerns_item_data)

            concerns.append(concerns_item)

        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = UpdateAgentBodyConfigActionsItem.from_dict(actions_item_data)

            actions.append(actions_item)

        _budget = d.pop("budget", UNSET)
        budget: Union[Unset, UpdateAgentBodyConfigBudget]
        if isinstance(_budget, Unset):
            budget = UNSET
        else:
            budget = UpdateAgentBodyConfigBudget.from_dict(_budget)

        outputs = []
        _outputs = d.pop("outputs", UNSET)
        for outputs_item_data in _outputs or []:
            outputs_item = UpdateAgentBodyConfigOutputsItem.from_dict(outputs_item_data)

            outputs.append(outputs_item)

        update_agent_body_config = cls(
            concerns=concerns,
            actions=actions,
            budget=budget,
            outputs=outputs,
        )

        return update_agent_body_config
