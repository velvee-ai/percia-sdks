from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.camera_pull_reason_type_1 import CameraPullReasonType1
from ..models.camera_pull_state_type_1 import CameraPullStateType1
from ..types import UNSET, Unset

T = TypeVar("T", bound="CameraPull")


@_attrs_define
class CameraPull:
    """link and file cameras only: the last report of the puller. Never an address.

    Attributes:
        reason (Union[CameraPullReasonType1, None, Unset]):
        state (Union[CameraPullStateType1, None, Unset]):
    """

    reason: Union[CameraPullReasonType1, None, Unset] = UNSET
    state: Union[CameraPullStateType1, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        elif isinstance(self.reason, CameraPullReasonType1):
            reason = self.reason.value
        else:
            reason = self.reason

        state: Union[None, Unset, str]
        if isinstance(self.state, Unset):
            state = UNSET
        elif isinstance(self.state, CameraPullStateType1):
            state = self.state.value
        else:
            state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reason is not UNSET:
            field_dict["reason"] = reason
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_reason(data: object) -> Union[CameraPullReasonType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_1 = CameraPullReasonType1(data)

                return reason_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CameraPullReasonType1, None, Unset], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_state(data: object) -> Union[CameraPullStateType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_1 = CameraPullStateType1(data)

                return state_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CameraPullStateType1, None, Unset], data)

        state = _parse_state(d.pop("state", UNSET))

        camera_pull = cls(
            reason=reason,
            state=state,
        )

        camera_pull.additional_properties = d
        return camera_pull

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
