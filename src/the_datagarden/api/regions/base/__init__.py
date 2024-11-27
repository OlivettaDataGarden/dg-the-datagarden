from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from the_datagarden.api.authentication.settings import INCLUDE_STATISTIC_PARAM
from the_datagarden.api.base import BaseApi

from .settings import ResponseKeys


class PeriodTypes:
    """Choice class for periodtype used in most data classes"""

    YEAR = "Y"
    QUARTER = "Q"
    MONTH = "M"
    WEEK = "W"
    DAY = "D"
    HOUR = "H"


PeriodType = Literal["Y", "Q", "M", "W", "D", "H"]


class RegionParams(BaseModel):
    models: list[str] | None = None
    source: list[str] | None = None
    period_type: PeriodType = "Y"
    period_from: datetime | None = None
    period_to: datetime | None = None
    region_type: str | None = None
    descendant_level: int = 0


class Region:
    """
    A region in The Data Garden.
    """

    _info: dict = {}
    _available_models: list[str] = []
    KEYS: type[StrEnum]

    def __init__(self, url: str, api: BaseApi):
        self._url = url
        self._api = api

    @property
    def info(self) -> dict | None:
        """
        Get the region info from the API.
        """
        if not self._info:
            info_resp = self._api.retrieve_from_api(
                url_extension=self._url,
                params=INCLUDE_STATISTIC_PARAM,
            )
            if info_resp.status_code == 200:
                info_resp_json = info_resp.json()
                self._info = info_resp_json if isinstance(info_resp_json, dict) else {}

        return self._info

    def available_models(self) -> list[str]:
        if self.info:
            return self.info.get(self._key(ResponseKeys.AVAILABLE_MODELS), [])
        return []

    def generic_regional_data(self) -> dict | None:
        meta_data_resp = self._api.retrieve_from_api(
            url_extension=self._url + "regional_data/",
            method="POST",
        )
        if meta_data_resp:
            return meta_data_resp.json()
        return None

    def _key(self, key: str) -> str:
        return getattr(self.KEYS, key)
