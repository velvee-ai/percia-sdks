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
    from ..models.update_agent_body_config import UpdateAgentBodyConfig


T = TypeVar("T", bound="UpdateAgentBody")


@_attrs_define
class UpdateAgentBody:
    """
    Attributes:
        config (Union[Unset, UpdateAgentBodyConfig]):
        name (Union[Unset, str]):
    """

    config: Union[Unset, "UpdateAgentBodyConfig"] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_agent_body_config import UpdateAgentBodyConfig

        d = dict(src_dict)
        _config = d.pop("config", UNSET)
        config: Union[Unset, UpdateAgentBodyConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = UpdateAgentBodyConfig.from_dict(_config)

        name = d.pop("name", UNSET)

        update_agent_body = cls(
            config=config,
            name=name,
        )

        update_agent_body.additional_properties = d
        return update_agent_body

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
