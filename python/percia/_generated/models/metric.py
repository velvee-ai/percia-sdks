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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_events_per_day_item import MetricEventsPerDayItem
    from ..models.metric_feedback import MetricFeedback


T = TypeVar("T", bound="Metric")


@_attrs_define
class Metric:
    """
    Attributes:
        events (Union[Unset, int]):
        events_per_day (Union[Unset, list['MetricEventsPerDayItem']]):
        false_alarm_rate (Union[None, Unset, float]):
        feedback (Union[Unset, MetricFeedback]):
        id (Union[Unset, str]):
        last_test_pass_rate (Union[None, Unset, float]):
    """

    events: Union[Unset, int] = UNSET
    events_per_day: Union[Unset, list["MetricEventsPerDayItem"]] = UNSET
    false_alarm_rate: Union[None, Unset, float] = UNSET
    feedback: Union[Unset, "MetricFeedback"] = UNSET
    id: Union[Unset, str] = UNSET
    last_test_pass_rate: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        events = self.events

        events_per_day: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.events_per_day, Unset):
            events_per_day = []
            for events_per_day_item_data in self.events_per_day:
                events_per_day_item = events_per_day_item_data.to_dict()
                events_per_day.append(events_per_day_item)

        false_alarm_rate: Union[None, Unset, float]
        if isinstance(self.false_alarm_rate, Unset):
            false_alarm_rate = UNSET
        else:
            false_alarm_rate = self.false_alarm_rate

        feedback: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.feedback, Unset):
            feedback = self.feedback.to_dict()

        id = self.id

        last_test_pass_rate: Union[None, Unset, float]
        if isinstance(self.last_test_pass_rate, Unset):
            last_test_pass_rate = UNSET
        else:
            last_test_pass_rate = self.last_test_pass_rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if events is not UNSET:
            field_dict["events"] = events
        if events_per_day is not UNSET:
            field_dict["eventsPerDay"] = events_per_day
        if false_alarm_rate is not UNSET:
            field_dict["falseAlarmRate"] = false_alarm_rate
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if id is not UNSET:
            field_dict["id"] = id
        if last_test_pass_rate is not UNSET:
            field_dict["lastTestPassRate"] = last_test_pass_rate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_events_per_day_item import MetricEventsPerDayItem
        from ..models.metric_feedback import MetricFeedback

        d = dict(src_dict)
        events = d.pop("events", UNSET)

        events_per_day = []
        _events_per_day = d.pop("eventsPerDay", UNSET)
        for events_per_day_item_data in _events_per_day or []:
            events_per_day_item = MetricEventsPerDayItem.from_dict(events_per_day_item_data)

            events_per_day.append(events_per_day_item)

        def _parse_false_alarm_rate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        false_alarm_rate = _parse_false_alarm_rate(d.pop("falseAlarmRate", UNSET))

        _feedback = d.pop("feedback", UNSET)
        feedback: Union[Unset, MetricFeedback]
        if isinstance(_feedback, Unset):
            feedback = UNSET
        else:
            feedback = MetricFeedback.from_dict(_feedback)

        id = d.pop("id", UNSET)

        def _parse_last_test_pass_rate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        last_test_pass_rate = _parse_last_test_pass_rate(d.pop("lastTestPassRate", UNSET))

        metric = cls(
            events=events,
            events_per_day=events_per_day,
            false_alarm_rate=false_alarm_rate,
            feedback=feedback,
            id=id,
            last_test_pass_rate=last_test_pass_rate,
        )

        metric.additional_properties = d
        return metric

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
