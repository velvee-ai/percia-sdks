from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RunAgentTestsBody")


@_attrs_define
class RunAgentTestsBody:
    """
    Attributes:
        version (Union[Literal['draft'], int]):
    """

    version: Union[Literal["draft"], int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version: Union[Literal["draft"], int]
        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_version(data: object) -> Union[Literal["draft"], int]:
            version_type_0 = cast(Literal["draft"], data)
            if version_type_0 != "draft":
                raise ValueError(f"version_type_0 must match const 'draft', got '{version_type_0}'")
            return version_type_0
            return cast(Union[Literal["draft"], int], data)

        version = _parse_version(d.pop("version"))

        run_agent_tests_body = cls(
            version=version,
        )

        run_agent_tests_body.additional_properties = d
        return run_agent_tests_body

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
