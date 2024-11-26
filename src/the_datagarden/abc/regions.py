from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from .api import BaseApi


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

    _available_models: list[str] = []

    def __init__(self, url: str, api: BaseApi):
        self._url = url
        self._api = api

    def info(self) -> dict | None:
        """
        Get the region info from the API.
        """
        info_resp = self._api.retrieve_from_api(
            url_extension=self._url,
        )
        if info_resp:
            return info_resp.json()
        return None

    def generic_regional_data(self) -> dict | None:
        meta_data_resp = self._api.retrieve_from_api(
            url_extension=self._url + "regional_data/",
            method="POST",
        )
        if meta_data_resp:
            return meta_data_resp.json()
        return None
