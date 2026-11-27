from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_whoami_response_200_credential import GetWhoamiResponse200Credential
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetWhoamiResponse200")


@_attrs_define
class GetWhoamiResponse200:
    """
    Attributes:
        credential (GetWhoamiResponse200Credential):
        scopes (Union[None, list[str]]): null for a session.
        user_id (str):
        account (Union[None, Unset, str]): Masked, such as j***@example.com.
        app_name (Union[None, Unset, str]):
        email (Union[Unset, str]):
        key_name (Union[Unset, str]):
    """

    credential: GetWhoamiResponse200Credential
    scopes: Union[None, list[str]]
    user_id: str
    account: Union[None, Unset, str] = UNSET
    app_name: Union[None, Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    key_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        credential = self.credential.value

        scopes: Union[None, list[str]]
        if isinstance(self.scopes, list):
            scopes = self.scopes

        else:
            scopes = self.scopes

        user_id = self.user_id

        account: Union[None, Unset, str]
        if isinstance(self.account, Unset):
            account = UNSET
        else:
            account = self.account

        app_name: Union[None, Unset, str]
        if isinstance(self.app_name, Unset):
            app_name = UNSET
        else:
            app_name = self.app_name

        email = self.email

        key_name = self.key_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "credential": credential,
                "scopes": scopes,
                "userId": user_id,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if app_name is not UNSET:
            field_dict["appName"] = app_name
        if email is not UNSET:
            field_dict["email"] = email
        if key_name is not UNSET:
            field_dict["keyName"] = key_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credential = GetWhoamiResponse200Credential(d.pop("credential"))

        def _parse_scopes(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scopes_type_0 = cast(list[str], data)

                return scopes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        scopes = _parse_scopes(d.pop("scopes"))

        user_id = d.pop("userId")

        def _parse_account(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        account = _parse_account(d.pop("account", UNSET))

        def _parse_app_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        app_name = _parse_app_name(d.pop("appName", UNSET))

        email = d.pop("email", UNSET)

        key_name = d.pop("keyName", UNSET)

        get_whoami_response_200 = cls(
            credential=credential,
            scopes=scopes,
            user_id=user_id,
            account=account,
            app_name=app_name,
            email=email,
            key_name=key_name,
        )

        get_whoami_response_200.additional_properties = d
        return get_whoami_response_200

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
