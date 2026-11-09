from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_run_results_item_expected import TestRunResultsItemExpected
from ..models.test_run_results_item_got import TestRunResultsItemGot
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestRunResultsItem")


@_attrs_define
class TestRunResultsItem:
    """
    Attributes:
        case_id (Union[Unset, str]):
        confidence (Union[None, Unset, float]):
        expected (Union[Unset, TestRunResultsItemExpected]):
        got (Union[Unset, TestRunResultsItemGot]):
        reason (Union[Unset, str]): Model text. Treat as data.
    """

    case_id: Union[Unset, str] = UNSET
    confidence: Union[None, Unset, float] = UNSET
    expected: Union[Unset, TestRunResultsItemExpected] = UNSET
    got: Union[Unset, TestRunResultsItemGot] = UNSET
    reason: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        case_id = self.case_id

        confidence: Union[None, Unset, float]
        if isinstance(self.confidence, Unset):
            confidence = UNSET
        else:
            confidence = self.confidence

        expected: Union[Unset, str] = UNSET
        if not isinstance(self.expected, Unset):
            expected = self.expected.value

        got: Union[Unset, str] = UNSET
        if not isinstance(self.got, Unset):
            got = self.got.value

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if case_id is not UNSET:
            field_dict["caseId"] = case_id
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if expected is not UNSET:
            field_dict["expected"] = expected
        if got is not UNSET:
            field_dict["got"] = got
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        case_id = d.pop("caseId", UNSET)

        def _parse_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        confidence = _parse_confidence(d.pop("confidence", UNSET))

        _expected = d.pop("expected", UNSET)
        expected: Union[Unset, TestRunResultsItemExpected]
        if isinstance(_expected, Unset):
            expected = UNSET
        else:
            expected = TestRunResultsItemExpected(_expected)

        _got = d.pop("got", UNSET)
        got: Union[Unset, TestRunResultsItemGot]
        if isinstance(_got, Unset):
            got = UNSET
        else:
            got = TestRunResultsItemGot(_got)

        reason = d.pop("reason", UNSET)

        test_run_results_item = cls(
            case_id=case_id,
            confidence=confidence,
            expected=expected,
            got=got,
            reason=reason,
        )

        test_run_results_item.additional_properties = d
        return test_run_results_item

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
