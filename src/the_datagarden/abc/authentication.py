from abc import ABC, abstractmethod
from typing import TypedDict


class TheDatagardenCredentialsDict(TypedDict):
    email: str
    password: str


class BaseDataGardenCredentials(ABC):
    """Protocol for the datagarden credentials"""

    @classmethod
    @abstractmethod
    def credentials(
        cls, the_datagarden_api_url: str, email: str | None = None, password: str | None = None
    ) -> TheDatagardenCredentialsDict: ...


class DatagardenEnvironment(ABC):
    """Protocol for the datagarden environment"""

    CREDENTIALS: type[BaseDataGardenCredentials]
    THE_DATAGARDEN_URL: str

    def credentials(
        self, email: str | None = None, password: str | None = None
    ) -> TheDatagardenCredentialsDict:
        return self.CREDENTIALS.credentials(self.the_datagarden_url, email, password)

    @property
    def the_datagarden_url(self) -> str:
        url = self.THE_DATAGARDEN_URL
        if url[-1] != "/":
            return url + "/"
        return url
