from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostSignalsBodySignalsItem")


@_attrs_define
class PostSignalsBodySignalsItem:
    """
    Attributes:
        channel (str):
        t_utc (str): The machine's clock, RFC 3339 UTC.
        value (Union[bool, float, str]):
        camera_id (Union[Unset, str]):
        seq (Union[Unset, int]):
        site_id (Union[Unset, str]):
    """

    channel: str
    t_utc: str
    value: Union[bool, float, str]
    camera_id: Union[Unset, str] = UNSET
    seq: Union[Unset, int] = UNSET
    site_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel = self.channel

        t_utc = self.t_utc

        value: Union[bool, float, str]
        value = self.value

        camera_id = self.camera_id

        seq = self.seq

        site_id = self.site_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel": channel,
                "t_utc": t_utc,
                "value": value,
            }
        )
        if camera_id is not UNSET:
            field_dict["camera_id"] = camera_id
        if seq is not UNSET:
            field_dict["seq"] = seq
        if site_id is not UNSET:
            field_dict["site_id"] = site_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel = d.pop("channel")

        t_utc = d.pop("t_utc")

        def _parse_value(data: object) -> Union[bool, float, str]:
            return cast(Union[bool, float, str], data)

        value = _parse_value(d.pop("value"))

        camera_id = d.pop("camera_id", UNSET)

        seq = d.pop("seq", UNSET)

        site_id = d.pop("site_id", UNSET)

        post_signals_body_signals_item = cls(
            channel=channel,
            t_utc=t_utc,
            value=value,
            camera_id=camera_id,
            seq=seq,
            site_id=site_id,
        )

        post_signals_body_signals_item.additional_properties = d
        return post_signals_body_signals_item

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
