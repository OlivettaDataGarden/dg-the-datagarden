import json
from datetime import UTC, datetime, timedelta

import jwt
import requests
from requests import Response

from ...abc.authentication import DatagardenEnvironment
from .settings import (
    BEARER_KEY,
    DEFAULT_HEADER,
    REFRESH_TOKEN_URL_EXTENSION,
    REQ_TOKEN_URL_EXTENSION,
)


class AccessToken:
    _instance = None
    _tokens: dict = {}
    TOKEN_LIFE_TIME_MARGIN: int = 20
    ACCESS_TOKEN_KEY = "access"
    REFRESH_TOKEN_KEY = "refresh"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        environment: type[DatagardenEnvironment],
        email: str | None = None,
        password: str | None = None,
    ) -> None:
        self._environment = environment()
        self._token_payload = self._environment.credentials(email, password)
        self._token_header = DEFAULT_HEADER.copy()

    @property
    def _token_url(self) -> str:
        return self._the_datagarden_url + REQ_TOKEN_URL_EXTENSION

    @property
    def _refresh_token_url(self) -> str:
        return self._the_datagarden_url + REFRESH_TOKEN_URL_EXTENSION

    @property
    def _the_datagarden_url(self) -> str:
        return self._environment.the_datagarden_url

    def _access_token_expired(self) -> bool:
        if self._token_expiry_time:
            return datetime.now(tz=UTC) + timedelta(seconds=5) > self._token_expiry_time
        return True

    @property
    def _access_token(self) -> str:
        if not self._tokens:
            self._request_tokens()
        elif self._access_token_expired():
            self._get_refresh_token()
        return self._tokens.get(self.ACCESS_TOKEN_KEY, "")

    @property
    def header_with_access_token(self) -> dict[str, str]:
        header = DEFAULT_HEADER.copy()
        header["Authorization"] = BEARER_KEY + self._access_token
        return header

    def _request_tokens(self):
        response = requests.request(
            method="POST",
            url=self._token_url,
            headers=self._token_header,
            data=json.dumps(self._token_payload),
        )
        if not response.status_code == 200:
            print("Token request failed and returned error(s): ")
            print("    Errorr : ", response.json().get("detail", "No error details provided"))
            quit()

        self._tokens = self._get_response_data(response)
        self._set_token_expiry_time()

    def _get_refresh_token(self):
        response = requests.request(
            method="POST",
            url=self._refresh_token_url,
            headers=self._token_header,
            data=json.dumps(self._refresh_payload()),
        )
        if not response.status_code == 200:
            raise ValueError("Token request failed and returned error: " f"{response.text}")
        self._tokens = self._get_response_data(response)
        self._set_token_expiry_time()

    def _refresh_payload(self) -> dict:
        refresh_token = self._tokens.get(self.REFRESH_TOKEN_KEY, "")
        return {"refresh": refresh_token}

    def _set_token_expiry_time(self):
        if not self._tokens:
            return
        access_token = self._tokens.get(self.ACCESS_TOKEN_KEY, "")
        if not access_token:
            raise ValueError("Access token not found in response")
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        exp_time_stamp = decoded_token["exp"]
        self._token_expiry_time = datetime.fromtimestamp(timestamp=exp_time_stamp, tz=UTC)

    def _get_response_data(self, response: Response) -> dict[str, str]:
        return json.loads(response.text)
