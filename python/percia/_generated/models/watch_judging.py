import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.watch_judging_state import WatchJudgingState
from ..types import UNSET, Unset

T = TypeVar("T", bound="WatchJudging")


@_attrs_define
class WatchJudging:
    """Whether the pool is judging this watch (read-only, additive). `state`: judging (a judge call in the last 10
    minutes), waiting_for_change (video arrives and the picture is still, so nothing is judged; a state goal is still
    looked at about every 5 minutes), no_video, paused (see `reason`), over_budget (the hourly judge limit skipped
    calls), judge_unavailable, starting (also: no frames yet, for up to 4 minutes after the pool started the watch;
    noVideoSince reads null then), not_running (no container reports) or unknown (core runtime). A confirmed no-alert is
    `judging` or `waiting_for_change` with a recent lastFrameAt: silence with state not_running or no_video means
    nothing was watched. `stalled` is true when video flows and a scheduled judge call is 15+ minutes overdue.

        Attributes:
            frames_received (Union[None, Unset, int]): Frames the current container has received.
            judge_calls_last_hour (Union[None, Unset, int]):
            judge_calls_today (Union[None, Unset, int]): UTC day.
            last_decision_at (Union[None, Unset, datetime.datetime]):
            last_frame_at (Union[None, Unset, datetime.datetime]):
            last_judged_at (Union[None, Unset, datetime.datetime]): Last successful judge call.
            limit_per_hour (Union[None, Unset, int]):
            reason (Union[None, Unset, str]): pausedReason when paused.
            reported_at (Union[None, Unset, datetime.datetime]): When the container last reported (about every 30 s).
            stalled (Union[Unset, bool]):
            state (Union[Unset, WatchJudgingState]):
    """

    frames_received: Union[None, Unset, int] = UNSET
    judge_calls_last_hour: Union[None, Unset, int] = UNSET
    judge_calls_today: Union[None, Unset, int] = UNSET
    last_decision_at: Union[None, Unset, datetime.datetime] = UNSET
    last_frame_at: Union[None, Unset, datetime.datetime] = UNSET
    last_judged_at: Union[None, Unset, datetime.datetime] = UNSET
    limit_per_hour: Union[None, Unset, int] = UNSET
    reason: Union[None, Unset, str] = UNSET
    reported_at: Union[None, Unset, datetime.datetime] = UNSET
    stalled: Union[Unset, bool] = UNSET
    state: Union[Unset, WatchJudgingState] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        frames_received: Union[None, Unset, int]
        if isinstance(self.frames_received, Unset):
            frames_received = UNSET
        else:
            frames_received = self.frames_received

        judge_calls_last_hour: Union[None, Unset, int]
        if isinstance(self.judge_calls_last_hour, Unset):
            judge_calls_last_hour = UNSET
        else:
            judge_calls_last_hour = self.judge_calls_last_hour

        judge_calls_today: Union[None, Unset, int]
        if isinstance(self.judge_calls_today, Unset):
            judge_calls_today = UNSET
        else:
            judge_calls_today = self.judge_calls_today

        last_decision_at: Union[None, Unset, str]
        if isinstance(self.last_decision_at, Unset):
            last_decision_at = UNSET
        elif isinstance(self.last_decision_at, datetime.datetime):
            last_decision_at = self.last_decision_at.isoformat()
        else:
            last_decision_at = self.last_decision_at

        last_frame_at: Union[None, Unset, str]
        if isinstance(self.last_frame_at, Unset):
            last_frame_at = UNSET
        elif isinstance(self.last_frame_at, datetime.datetime):
            last_frame_at = self.last_frame_at.isoformat()
        else:
            last_frame_at = self.last_frame_at

        last_judged_at: Union[None, Unset, str]
        if isinstance(self.last_judged_at, Unset):
            last_judged_at = UNSET
        elif isinstance(self.last_judged_at, datetime.datetime):
            last_judged_at = self.last_judged_at.isoformat()
        else:
            last_judged_at = self.last_judged_at

        limit_per_hour: Union[None, Unset, int]
        if isinstance(self.limit_per_hour, Unset):
            limit_per_hour = UNSET
        else:
            limit_per_hour = self.limit_per_hour

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        reported_at: Union[None, Unset, str]
        if isinstance(self.reported_at, Unset):
            reported_at = UNSET
        elif isinstance(self.reported_at, datetime.datetime):
            reported_at = self.reported_at.isoformat()
        else:
            reported_at = self.reported_at

        stalled = self.stalled

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if frames_received is not UNSET:
            field_dict["framesReceived"] = frames_received
        if judge_calls_last_hour is not UNSET:
            field_dict["judgeCallsLastHour"] = judge_calls_last_hour
        if judge_calls_today is not UNSET:
            field_dict["judgeCallsToday"] = judge_calls_today
        if last_decision_at is not UNSET:
            field_dict["lastDecisionAt"] = last_decision_at
        if last_frame_at is not UNSET:
            field_dict["lastFrameAt"] = last_frame_at
        if last_judged_at is not UNSET:
            field_dict["lastJudgedAt"] = last_judged_at
        if limit_per_hour is not UNSET:
            field_dict["limitPerHour"] = limit_per_hour
        if reason is not UNSET:
            field_dict["reason"] = reason
        if reported_at is not UNSET:
            field_dict["reportedAt"] = reported_at
        if stalled is not UNSET:
            field_dict["stalled"] = stalled
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_frames_received(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        frames_received = _parse_frames_received(d.pop("framesReceived", UNSET))

        def _parse_judge_calls_last_hour(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        judge_calls_last_hour = _parse_judge_calls_last_hour(d.pop("judgeCallsLastHour", UNSET))

        def _parse_judge_calls_today(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        judge_calls_today = _parse_judge_calls_today(d.pop("judgeCallsToday", UNSET))

        def _parse_last_decision_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_decision_at_type_0 = isoparse(data)

                return last_decision_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_decision_at = _parse_last_decision_at(d.pop("lastDecisionAt", UNSET))

        def _parse_last_frame_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_frame_at_type_0 = isoparse(data)

                return last_frame_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_frame_at = _parse_last_frame_at(d.pop("lastFrameAt", UNSET))

        def _parse_last_judged_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_judged_at_type_0 = isoparse(data)

                return last_judged_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_judged_at = _parse_last_judged_at(d.pop("lastJudgedAt", UNSET))

        def _parse_limit_per_hour(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        limit_per_hour = _parse_limit_per_hour(d.pop("limitPerHour", UNSET))

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_reported_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reported_at_type_0 = isoparse(data)

                return reported_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        reported_at = _parse_reported_at(d.pop("reportedAt", UNSET))

        stalled = d.pop("stalled", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, WatchJudgingState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = WatchJudgingState(_state)

        watch_judging = cls(
            frames_received=frames_received,
            judge_calls_last_hour=judge_calls_last_hour,
            judge_calls_today=judge_calls_today,
            last_decision_at=last_decision_at,
            last_frame_at=last_frame_at,
            last_judged_at=last_judged_at,
            limit_per_hour=limit_per_hour,
            reason=reason,
            reported_at=reported_at,
            stalled=stalled,
            state=state,
        )

        watch_judging.additional_properties = d
        return watch_judging

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
