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
    from ..models.post_signals_body_signals_item import PostSignalsBodySignalsItem


T = TypeVar("T", bound="PostSignalsBody")


@_attrs_define
class PostSignalsBody:
    """
    Attributes:
        signals (list['PostSignalsBodySignalsItem']):
        camera_id (Union[Unset, str]): Default camera for the signals that name none.
        site_id (Union[Unset, str]): Default site for the signals that name none (a signal with only a site goes to the
            site's stream).
    """

    signals: list["PostSignalsBodySignalsItem"]
    camera_id: Union[Unset, str] = UNSET
    site_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        signals = []
        for signals_item_data in self.signals:
            signals_item = signals_item_data.to_dict()
            signals.append(signals_item)

        camera_id = self.camera_id

        site_id = self.site_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "signals": signals,
            }
        )
        if camera_id is not UNSET:
            field_dict["cameraId"] = camera_id
        if site_id is not UNSET:
            field_dict["siteId"] = site_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_signals_body_signals_item import PostSignalsBodySignalsItem

        d = dict(src_dict)
        signals = []
        _signals = d.pop("signals")
        for signals_item_data in _signals:
            signals_item = PostSignalsBodySignalsItem.from_dict(signals_item_data)

            signals.append(signals_item)

        camera_id = d.pop("cameraId", UNSET)

        site_id = d.pop("siteId", UNSET)

        post_signals_body = cls(
            signals=signals,
            camera_id=camera_id,
            site_id=site_id,
        )

        post_signals_body.additional_properties = d
        return post_signals_body

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
