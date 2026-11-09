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

T = TypeVar("T", bound="ConnectWithTwilioBody")


@_attrs_define
class ConnectWithTwilioBody:
    """
    Attributes:
        account_sid (str):
        secret (str):
        sender (str):
        to (str):
        api_key_sid (Union[Unset, str]):
        content_sid (Union[Unset, str]):
        default (Union[Unset, bool]):
        label (Union[Unset, str]):
        limit_per_hour (Union[Unset, float, str]):
        mms (Union[Unset, bool]):
        variables (Union[Unset, list[str], str]):
    """

    account_sid: str
    secret: str
    sender: str
    to: str
    api_key_sid: Union[Unset, str] = UNSET
    content_sid: Union[Unset, str] = UNSET
    default: Union[Unset, bool] = UNSET
    label: Union[Unset, str] = UNSET
    limit_per_hour: Union[Unset, float, str] = UNSET
    mms: Union[Unset, bool] = UNSET
    variables: Union[Unset, list[str], str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_sid = self.account_sid

        secret = self.secret

        sender = self.sender

        to = self.to

        api_key_sid = self.api_key_sid

        content_sid = self.content_sid

        default = self.default

        label = self.label

        limit_per_hour: Union[Unset, float, str]
        if isinstance(self.limit_per_hour, Unset):
            limit_per_hour = UNSET
        else:
            limit_per_hour = self.limit_per_hour

        mms = self.mms

        variables: Union[Unset, list[str], str]
        if isinstance(self.variables, Unset):
            variables = UNSET
        elif isinstance(self.variables, list):
            variables = self.variables

        else:
            variables = self.variables

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountSid": account_sid,
                "secret": secret,
                "sender": sender,
                "to": to,
            }
        )
        if api_key_sid is not UNSET:
            field_dict["apiKeySid"] = api_key_sid
        if content_sid is not UNSET:
            field_dict["contentSid"] = content_sid
        if default is not UNSET:
            field_dict["default"] = default
        if label is not UNSET:
            field_dict["label"] = label
        if limit_per_hour is not UNSET:
            field_dict["limitPerHour"] = limit_per_hour
        if mms is not UNSET:
            field_dict["mms"] = mms
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        account_sid = d.pop("accountSid")

        secret = d.pop("secret")

        sender = d.pop("sender")

        to = d.pop("to")

        api_key_sid = d.pop("apiKeySid", UNSET)

        content_sid = d.pop("contentSid", UNSET)

        default = d.pop("default", UNSET)

        label = d.pop("label", UNSET)

        def _parse_limit_per_hour(data: object) -> Union[Unset, float, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, float, str], data)

        limit_per_hour = _parse_limit_per_hour(d.pop("limitPerHour", UNSET))

        mms = d.pop("mms", UNSET)

        def _parse_variables(data: object) -> Union[Unset, list[str], str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                variables_type_1 = cast(list[str], data)

                return variables_type_1
            except:  # noqa: E722
                pass
            return cast(Union[Unset, list[str], str], data)

        variables = _parse_variables(d.pop("variables", UNSET))

        connect_with_twilio_body = cls(
            account_sid=account_sid,
            secret=secret,
            sender=sender,
            to=to,
            api_key_sid=api_key_sid,
            content_sid=content_sid,
            default=default,
            label=label,
            limit_per_hour=limit_per_hour,
            mms=mms,
            variables=variables,
        )

        connect_with_twilio_body.additional_properties = d
        return connect_with_twilio_body

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
