import datetime
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
from dateutil.parser import isoparse

from ..models.get_test_run_response_200_judge_type_1 import (
    GetTestRunResponse200JudgeType1,
)
from ..models.get_test_run_response_200_source import GetTestRunResponse200Source
from ..models.get_test_run_response_200_status import GetTestRunResponse200Status
from ..models.get_test_run_response_200_verdict_type_1 import (
    GetTestRunResponse200VerdictType1,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_test_run_response_200_alerts_item import (
        GetTestRunResponse200AlertsItem,
    )
    from ..models.get_test_run_response_200_capability_item import (
        GetTestRunResponse200CapabilityItem,
    )
    from ..models.get_test_run_response_200_caught_type_0 import (
        GetTestRunResponse200CaughtType0,
    )
    from ..models.get_test_run_response_200_clips_item import (
        GetTestRunResponse200ClipsItem,
    )
    from ..models.get_test_run_response_200_coverage import (
        GetTestRunResponse200Coverage,
    )
    from ..models.get_test_run_response_200_false_alarms_type_0 import (
        GetTestRunResponse200FalseAlarmsType0,
    )
    from ..models.get_test_run_response_200_scores import GetTestRunResponse200Scores
    from ..models.get_test_run_response_200_window_type_0 import (
        GetTestRunResponse200WindowType0,
    )


T = TypeVar("T", bound="GetTestRunResponse200")


@_attrs_define
class GetTestRunResponse200:
    """
    Attributes:
        alerts (Union[Unset, list['GetTestRunResponse200AlertsItem']]):
        capability (Union[Unset, list['GetTestRunResponse200CapabilityItem']]):
        caught (Union['GetTestRunResponse200CaughtType0', None, Unset]):
        clip_count (Union[Unset, int]):
        clips (Union[Unset, list['GetTestRunResponse200ClipsItem']]):
        coverage (Union[Unset, GetTestRunResponse200Coverage]):
        created_at (Union[Unset, datetime.datetime]):
        engine (Union[None, Unset, str]):
        error (Union[None, Unset, str]):
        false_alarms (Union['GetTestRunResponse200FalseAlarmsType0', None, Unset]):
        finished_at (Union[None, Unset, datetime.datetime]):
        id (Union[Unset, str]):
        judge (Union[GetTestRunResponse200JudgeType1, None, Unset]):
        scores (Union[Unset, GetTestRunResponse200Scores]): caught, falseAlarms and avgDelayS are figures or null; each
            null has a *Note saying why it is unmeasured. verdict is ready, review or unmeasured with verdictWhy (the stated
            rule: ready needs at least 3 should_match and 1 should_not or counterfactual clip, all caught, no false alarm).
        source (Union[Unset, GetTestRunResponse200Source]):
        spend_usd (Union[None, Unset, float]):
        status (Union[Unset, GetTestRunResponse200Status]):
        verdict (Union[GetTestRunResponse200VerdictType1, None, Unset]):
        window (Union['GetTestRunResponse200WindowType0', None, Unset]):
    """

    alerts: Union[Unset, list["GetTestRunResponse200AlertsItem"]] = UNSET
    capability: Union[Unset, list["GetTestRunResponse200CapabilityItem"]] = UNSET
    caught: Union["GetTestRunResponse200CaughtType0", None, Unset] = UNSET
    clip_count: Union[Unset, int] = UNSET
    clips: Union[Unset, list["GetTestRunResponse200ClipsItem"]] = UNSET
    coverage: Union[Unset, "GetTestRunResponse200Coverage"] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    engine: Union[None, Unset, str] = UNSET
    error: Union[None, Unset, str] = UNSET
    false_alarms: Union["GetTestRunResponse200FalseAlarmsType0", None, Unset] = UNSET
    finished_at: Union[None, Unset, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET
    judge: Union[GetTestRunResponse200JudgeType1, None, Unset] = UNSET
    scores: Union[Unset, "GetTestRunResponse200Scores"] = UNSET
    source: Union[Unset, GetTestRunResponse200Source] = UNSET
    spend_usd: Union[None, Unset, float] = UNSET
    status: Union[Unset, GetTestRunResponse200Status] = UNSET
    verdict: Union[GetTestRunResponse200VerdictType1, None, Unset] = UNSET
    window: Union["GetTestRunResponse200WindowType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.get_test_run_response_200_caught_type_0 import (
            GetTestRunResponse200CaughtType0,
        )
        from ..models.get_test_run_response_200_false_alarms_type_0 import (
            GetTestRunResponse200FalseAlarmsType0,
        )
        from ..models.get_test_run_response_200_window_type_0 import (
            GetTestRunResponse200WindowType0,
        )

        alerts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.alerts, Unset):
            alerts = []
            for alerts_item_data in self.alerts:
                alerts_item = alerts_item_data.to_dict()
                alerts.append(alerts_item)

        capability: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.capability, Unset):
            capability = []
            for capability_item_data in self.capability:
                capability_item = capability_item_data.to_dict()
                capability.append(capability_item)

        caught: Union[None, Unset, dict[str, Any]]
        if isinstance(self.caught, Unset):
            caught = UNSET
        elif isinstance(self.caught, GetTestRunResponse200CaughtType0):
            caught = self.caught.to_dict()
        else:
            caught = self.caught

        clip_count = self.clip_count

        clips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.clips, Unset):
            clips = []
            for clips_item_data in self.clips:
                clips_item = clips_item_data.to_dict()
                clips.append(clips_item)

        coverage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.coverage, Unset):
            coverage = self.coverage.to_dict()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        engine: Union[None, Unset, str]
        if isinstance(self.engine, Unset):
            engine = UNSET
        else:
            engine = self.engine

        error: Union[None, Unset, str]
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        false_alarms: Union[None, Unset, dict[str, Any]]
        if isinstance(self.false_alarms, Unset):
            false_alarms = UNSET
        elif isinstance(self.false_alarms, GetTestRunResponse200FalseAlarmsType0):
            false_alarms = self.false_alarms.to_dict()
        else:
            false_alarms = self.false_alarms

        finished_at: Union[None, Unset, str]
        if isinstance(self.finished_at, Unset):
            finished_at = UNSET
        elif isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        id = self.id

        judge: Union[None, Unset, str]
        if isinstance(self.judge, Unset):
            judge = UNSET
        elif isinstance(self.judge, GetTestRunResponse200JudgeType1):
            judge = self.judge.value
        else:
            judge = self.judge

        scores: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.scores, Unset):
            scores = self.scores.to_dict()

        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        spend_usd: Union[None, Unset, float]
        if isinstance(self.spend_usd, Unset):
            spend_usd = UNSET
        else:
            spend_usd = self.spend_usd

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        verdict: Union[None, Unset, str]
        if isinstance(self.verdict, Unset):
            verdict = UNSET
        elif isinstance(self.verdict, GetTestRunResponse200VerdictType1):
            verdict = self.verdict.value
        else:
            verdict = self.verdict

        window: Union[None, Unset, dict[str, Any]]
        if isinstance(self.window, Unset):
            window = UNSET
        elif isinstance(self.window, GetTestRunResponse200WindowType0):
            window = self.window.to_dict()
        else:
            window = self.window

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alerts is not UNSET:
            field_dict["alerts"] = alerts
        if capability is not UNSET:
            field_dict["capability"] = capability
        if caught is not UNSET:
            field_dict["caught"] = caught
        if clip_count is not UNSET:
            field_dict["clipCount"] = clip_count
        if clips is not UNSET:
            field_dict["clips"] = clips
        if coverage is not UNSET:
            field_dict["coverage"] = coverage
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if engine is not UNSET:
            field_dict["engine"] = engine
        if error is not UNSET:
            field_dict["error"] = error
        if false_alarms is not UNSET:
            field_dict["falseAlarms"] = false_alarms
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at
        if id is not UNSET:
            field_dict["id"] = id
        if judge is not UNSET:
            field_dict["judge"] = judge
        if scores is not UNSET:
            field_dict["scores"] = scores
        if source is not UNSET:
            field_dict["source"] = source
        if spend_usd is not UNSET:
            field_dict["spendUsd"] = spend_usd
        if status is not UNSET:
            field_dict["status"] = status
        if verdict is not UNSET:
            field_dict["verdict"] = verdict
        if window is not UNSET:
            field_dict["window"] = window

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_test_run_response_200_alerts_item import (
            GetTestRunResponse200AlertsItem,
        )
        from ..models.get_test_run_response_200_capability_item import (
            GetTestRunResponse200CapabilityItem,
        )
        from ..models.get_test_run_response_200_caught_type_0 import (
            GetTestRunResponse200CaughtType0,
        )
        from ..models.get_test_run_response_200_clips_item import (
            GetTestRunResponse200ClipsItem,
        )
        from ..models.get_test_run_response_200_coverage import (
            GetTestRunResponse200Coverage,
        )
        from ..models.get_test_run_response_200_false_alarms_type_0 import (
            GetTestRunResponse200FalseAlarmsType0,
        )
        from ..models.get_test_run_response_200_scores import (
            GetTestRunResponse200Scores,
        )
        from ..models.get_test_run_response_200_window_type_0 import (
            GetTestRunResponse200WindowType0,
        )

        d = dict(src_dict)
        alerts = []
        _alerts = d.pop("alerts", UNSET)
        for alerts_item_data in _alerts or []:
            alerts_item = GetTestRunResponse200AlertsItem.from_dict(alerts_item_data)

            alerts.append(alerts_item)

        capability = []
        _capability = d.pop("capability", UNSET)
        for capability_item_data in _capability or []:
            capability_item = GetTestRunResponse200CapabilityItem.from_dict(capability_item_data)

            capability.append(capability_item)

        def _parse_caught(
            data: object,
        ) -> Union["GetTestRunResponse200CaughtType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                caught_type_0 = GetTestRunResponse200CaughtType0.from_dict(data)

                return caught_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetTestRunResponse200CaughtType0", None, Unset], data)

        caught = _parse_caught(d.pop("caught", UNSET))

        clip_count = d.pop("clipCount", UNSET)

        clips = []
        _clips = d.pop("clips", UNSET)
        for clips_item_data in _clips or []:
            clips_item = GetTestRunResponse200ClipsItem.from_dict(clips_item_data)

            clips.append(clips_item)

        _coverage = d.pop("coverage", UNSET)
        coverage: Union[Unset, GetTestRunResponse200Coverage]
        if isinstance(_coverage, Unset):
            coverage = UNSET
        else:
            coverage = GetTestRunResponse200Coverage.from_dict(_coverage)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_engine(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        engine = _parse_engine(d.pop("engine", UNSET))

        def _parse_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_false_alarms(
            data: object,
        ) -> Union["GetTestRunResponse200FalseAlarmsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                false_alarms_type_0 = GetTestRunResponse200FalseAlarmsType0.from_dict(data)

                return false_alarms_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetTestRunResponse200FalseAlarmsType0", None, Unset], data)

        false_alarms = _parse_false_alarms(d.pop("falseAlarms", UNSET))

        def _parse_finished_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = isoparse(data)

                return finished_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        finished_at = _parse_finished_at(d.pop("finishedAt", UNSET))

        id = d.pop("id", UNSET)

        def _parse_judge(
            data: object,
        ) -> Union[GetTestRunResponse200JudgeType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                judge_type_1 = GetTestRunResponse200JudgeType1(data)

                return judge_type_1
            except:  # noqa: E722
                pass
            return cast(Union[GetTestRunResponse200JudgeType1, None, Unset], data)

        judge = _parse_judge(d.pop("judge", UNSET))

        _scores = d.pop("scores", UNSET)
        scores: Union[Unset, GetTestRunResponse200Scores]
        if isinstance(_scores, Unset):
            scores = UNSET
        else:
            scores = GetTestRunResponse200Scores.from_dict(_scores)

        _source = d.pop("source", UNSET)
        source: Union[Unset, GetTestRunResponse200Source]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = GetTestRunResponse200Source(_source)

        def _parse_spend_usd(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        spend_usd = _parse_spend_usd(d.pop("spendUsd", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, GetTestRunResponse200Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GetTestRunResponse200Status(_status)

        def _parse_verdict(
            data: object,
        ) -> Union[GetTestRunResponse200VerdictType1, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                verdict_type_1 = GetTestRunResponse200VerdictType1(data)

                return verdict_type_1
            except:  # noqa: E722
                pass
            return cast(Union[GetTestRunResponse200VerdictType1, None, Unset], data)

        verdict = _parse_verdict(d.pop("verdict", UNSET))

        def _parse_window(
            data: object,
        ) -> Union["GetTestRunResponse200WindowType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                window_type_0 = GetTestRunResponse200WindowType0.from_dict(data)

                return window_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetTestRunResponse200WindowType0", None, Unset], data)

        window = _parse_window(d.pop("window", UNSET))

        get_test_run_response_200 = cls(
            alerts=alerts,
            capability=capability,
            caught=caught,
            clip_count=clip_count,
            clips=clips,
            coverage=coverage,
            created_at=created_at,
            engine=engine,
            error=error,
            false_alarms=false_alarms,
            finished_at=finished_at,
            id=id,
            judge=judge,
            scores=scores,
            source=source,
            spend_usd=spend_usd,
            status=status,
            verdict=verdict,
            window=window,
        )

        get_test_run_response_200.additional_properties = d
        return get_test_run_response_200

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
