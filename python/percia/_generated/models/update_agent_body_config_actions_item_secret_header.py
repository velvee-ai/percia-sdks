from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateAgentBodyConfigActionsItemSecretHeader")


@_attrs_define
class UpdateAgentBodyConfigActionsItemSecretHeader:
    """
    Attributes:
        name (str):
        enc (Union[Unset, str]):
        has_secret (Union[Unset, bool]):
        value (Union[Unset, str]):
    """

    name: str
    enc: Union[Unset, str] = UNSET
    has_secret: Union[Unset, bool] = UNSET
    value: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        enc = self.enc

        has_secret = self.has_secret

        value = self.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )
        if enc is not UNSET:
            field_dict["enc"] = enc
        if has_secret is not UNSET:
            field_dict["hasSecret"] = has_secret
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        enc = d.pop("enc", UNSET)

        has_secret = d.pop("hasSecret", UNSET)

        value = d.pop("value", UNSET)

        update_agent_body_config_actions_item_secret_header = cls(
            name=name,
            enc=enc,
            has_secret=has_secret,
            value=value,
        )

        return update_agent_body_config_actions_item_secret_header
