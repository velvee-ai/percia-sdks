from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.create_watch_body_advanced_actions_item_kind import (
    CreateWatchBodyAdvancedActionsItemKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWatchBodyAdvancedActionsItem")


@_attrs_define
class CreateWatchBodyAdvancedActionsItem:
    """
    Attributes:
        condition_id (str):
        kind (CreateWatchBodyAdvancedActionsItemKind):
        resume_ok (Union[Unset, bool]):
    """

    condition_id: str
    kind: CreateWatchBodyAdvancedActionsItemKind
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

        kind = CreateWatchBodyAdvancedActionsItemKind(d.pop("kind"))

        resume_ok = d.pop("resume_ok", UNSET)

        create_watch_body_advanced_actions_item = cls(
            condition_id=condition_id,
            kind=kind,
            resume_ok=resume_ok,
        )

        return create_watch_body_advanced_actions_item
