from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.update_site_memory_body_entities_item_state import (
    UpdateSiteMemoryBodyEntitiesItemState,
)

T = TypeVar("T", bound="UpdateSiteMemoryBodyEntitiesItem")


@_attrs_define
class UpdateSiteMemoryBodyEntitiesItem:
    """
    Attributes:
        key (str):
        kind (str):
        label (str):
        last_event_id (Union[None, str]):
        last_seen (str):
        since (str):
        state (UpdateSiteMemoryBodyEntitiesItemState):
    """

    key: str
    kind: str
    label: str
    last_event_id: Union[None, str]
    last_seen: str
    since: str
    state: UpdateSiteMemoryBodyEntitiesItemState

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        kind = self.kind

        label = self.label

        last_event_id: Union[None, str]
        last_event_id = self.last_event_id

        last_seen = self.last_seen

        since = self.since

        state = self.state.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "key": key,
                "kind": kind,
                "label": label,
                "lastEventId": last_event_id,
                "lastSeen": last_seen,
                "since": since,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        kind = d.pop("kind")

        label = d.pop("label")

        def _parse_last_event_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        last_event_id = _parse_last_event_id(d.pop("lastEventId"))

        last_seen = d.pop("lastSeen")

        since = d.pop("since")

        state = UpdateSiteMemoryBodyEntitiesItemState(d.pop("state"))

        update_site_memory_body_entities_item = cls(
            key=key,
            kind=kind,
            label=label,
            last_event_id=last_event_id,
            last_seen=last_seen,
            since=since,
            state=state,
        )

        return update_site_memory_body_entities_item
