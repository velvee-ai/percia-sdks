from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_public_watch_body_notify_type_0 import (
        CreatePublicWatchBodyNotifyType0,
    )
    from ..models.create_public_watch_body_notify_type_1 import (
        CreatePublicWatchBodyNotifyType1,
    )


T = TypeVar("T", bound="CreatePublicWatchBody")


@_attrs_define
class CreatePublicWatchBody:
    """
    Attributes:
        goal (str):
        notify (Union['CreatePublicWatchBodyNotifyType0', 'CreatePublicWatchBodyNotifyType1']):
        source_url (str):
    """

    goal: str
    notify: Union["CreatePublicWatchBodyNotifyType0", "CreatePublicWatchBodyNotifyType1"]
    source_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_public_watch_body_notify_type_0 import (
            CreatePublicWatchBodyNotifyType0,
        )

        goal = self.goal

        notify: dict[str, Any]
        if isinstance(self.notify, CreatePublicWatchBodyNotifyType0):
            notify = self.notify.to_dict()
        else:
            notify = self.notify.to_dict()

        source_url: str
        source_url = self.source_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "goal": goal,
                "notify": notify,
                "sourceUrl": source_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_public_watch_body_notify_type_0 import (
            CreatePublicWatchBodyNotifyType0,
        )
        from ..models.create_public_watch_body_notify_type_1 import (
            CreatePublicWatchBodyNotifyType1,
        )

        d = dict(src_dict)
        goal = d.pop("goal")

        def _parse_notify(
            data: object,
        ) -> Union["CreatePublicWatchBodyNotifyType0", "CreatePublicWatchBodyNotifyType1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                notify_type_0 = CreatePublicWatchBodyNotifyType0.from_dict(data)

                return notify_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            notify_type_1 = CreatePublicWatchBodyNotifyType1.from_dict(data)

            return notify_type_1

        notify = _parse_notify(d.pop("notify"))

        def _parse_source_url(data: object) -> str:
            return cast(str, data)

        source_url = _parse_source_url(d.pop("sourceUrl"))

        create_public_watch_body = cls(
            goal=goal,
            notify=notify,
            source_url=source_url,
        )

        create_public_watch_body.additional_properties = d
        return create_public_watch_body

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
