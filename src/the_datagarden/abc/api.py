from abc import ABC, abstractmethod

from requests import Response

from the_datagarden.abc.authentication import DatagardenEnvironment


class BaseApi(ABC):
    @abstractmethod
    def __init__(self, environment: type[DatagardenEnvironment] | None = None): ...

    @abstractmethod
    def retrieve_from_api(
        self,
        url_extension: str,
        method: str = "GET",
        payload: dict | None = None,
        params: dict | None = None,
    ) -> Response | None: ...
