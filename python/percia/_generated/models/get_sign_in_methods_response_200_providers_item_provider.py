from enum import Enum


class GetSignInMethodsResponse200ProvidersItemProvider(str, Enum):
    APPLE = "apple"
    GITHUB = "github"
    GOOGLE = "google"

    def __str__(self) -> str:
        return str(self.value)
