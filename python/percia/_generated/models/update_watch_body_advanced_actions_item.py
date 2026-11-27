from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.update_watch_body_advanced_actions_item_kind import (
    UpdateWatchBodyAdvancedActionsItemKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateWatchBodyAdvancedActionsItem")


@_attrs_define
class UpdateWatchBodyAdvancedActionsItem:
    """
    Attributes:
        condition_id (str):
        kind (UpdateWatchBodyAdvancedActionsItemKind):
        resume_ok (Union[Unset, bool]):
    """

    condition_id: str
    kind: UpdateWatchBodyAdvancedActionsItemKind
    resume_ok: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        condition_id = self.condition_id

        kind = self.kind.value

        resume_ok = self.resume_ok

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "condition_id": condition_id,
                "kind": kind,
            }
        )
        if resume_ok is not UNSET:
            field_dict["resume_ok"] = resume_ok

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        condition_id = d.pop("condition_id")

        kind = UpdateWatchBodyAdvancedActionsItemKind(d.pop("kind"))

        resume_ok = d.pop("resume_ok", UNSET)

        update_watch_body_advanced_actions_item = cls(
            condition_id=condition_id,
            kind=kind,
            resume_ok=resume_ok,
        )

        return update_watch_body_advanced_actions_item
