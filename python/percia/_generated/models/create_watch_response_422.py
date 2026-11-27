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
    from ..models.create_watch_response_422_error import CreateWatchResponse422Error
    from ..models.create_watch_response_422_guidance import (
        CreateWatchResponse422Guidance,
    )
    from ..models.create_watch_response_422_options_item import (
        CreateWatchResponse422OptionsItem,
    )


T = TypeVar("T", bound="CreateWatchResponse422")


@_attrs_define
class CreateWatchResponse422:
    """
    Attributes:
        draft_id (Union[Unset, str]):
        error (Union[Unset, CreateWatchResponse422Error]):
        guidance (Union[Unset, CreateWatchResponse422Guidance]):
        options (Union[Unset, list['CreateWatchResponse422OptionsItem']]):
        question (Union[Unset, str]):
    """

    draft_id: Union[Unset, str] = UNSET
    error: Union[Unset, "CreateWatchResponse422Error"] = UNSET
    guidance: Union[Unset, "CreateWatchResponse422Guidance"] = UNSET
    options: Union[Unset, list["CreateWatchResponse422OptionsItem"]] = UNSET
    question: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        draft_id = self.draft_id

        error: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        guidance: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.guidance, Unset):
            guidance = self.guidance.to_dict()

        options: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        question = self.question

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if draft_id is not UNSET:
            field_dict["draftId"] = draft_id
        if error is not UNSET:
            field_dict["error"] = error
        if guidance is not UNSET:
            field_dict["guidance"] = guidance
        if options is not UNSET:
            field_dict["options"] = options
        if question is not UNSET:
            field_dict["question"] = question

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_watch_response_422_error import CreateWatchResponse422Error
        from ..models.create_watch_response_422_guidance import (
            CreateWatchResponse422Guidance,
        )
        from ..models.create_watch_response_422_options_item import (
            CreateWatchResponse422OptionsItem,
        )

        d = dict(src_dict)
        draft_id = d.pop("draftId", UNSET)

        _error = d.pop("error", UNSET)
        error: Union[Unset, CreateWatchResponse422Error]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = CreateWatchResponse422Error.from_dict(_error)

        _guidance = d.pop("guidance", UNSET)
        guidance: Union[Unset, CreateWatchResponse422Guidance]
        if isinstance(_guidance, Unset):
            guidance = UNSET
        else:
            guidance = CreateWatchResponse422Guidance.from_dict(_guidance)

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = CreateWatchResponse422OptionsItem.from_dict(options_item_data)

            options.append(options_item)

        question = d.pop("question", UNSET)

        create_watch_response_422 = cls(
            draft_id=draft_id,
            error=error,
            guidance=guidance,
            options=options,
            question=question,
        )

        create_watch_response_422.additional_properties = d
        return create_watch_response_422

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
