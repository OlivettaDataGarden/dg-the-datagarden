from datetime import datetime
from enum import StrEnum
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel

from the_datagarden.api.authentication.settings import INCLUDE_STATISTIC_PARAM
from the_datagarden.api.base import BaseApi
from the_datagarden.models import TheDataGardenRegionalDataModel

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
    _available_models: dict = {}

    KEYS: type[StrEnum]

    def __init__(self, url: str, api: BaseApi):
        self._url = url
        self._api = api

    def __getattr__(self, attr: str, *args, **kwargs):
        if attr in self._api_model_names:
            return self._model_data_from_api(model=attr, **kwargs)

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

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

    @property
    def statistics(self) -> dict:
        if self.info:
            return self.info.get(self._key(ResponseKeys.STATISTICS), {})
        return {}

    def available_models_names(self) -> list[str]:
        if not self._available_models:
            self._set_available_models()
        return list(self._available_models.keys())

    def available_models(self) -> dict:
        if not self._available_models:
            self._set_available_models()

        return self._available_models

    @property
    def _api_model_names(self) -> list[str]:
        return [model.lower() for model in self.available_models()]

    def _set_available_models(self) -> None:
        if self._available_models:
            return

        if self.statistics:
            self._available_models = self.statistics.get(self._key(ResponseKeys.AVAILABLE_MODELS), [])
        return

    @lru_cache(maxsize=1000)  # noqa: B019
    def _model_data_from_api(self, model: str, **kwargs) -> TheDataGardenRegionalDataModel | None:
        model_data_resp = self._api.retrieve_from_api(
            url_extension=self._url + "regional_data/",
            method="POST",
            payload={"model": model, **kwargs},
        )
        if model_data_resp:
            return TheDataGardenRegionalDataModel(model_data_resp.json())
        return None

    def generic_regional_data(self, model: str, **kwargs) -> dict | None:
        meta_data_resp = self._api.retrieve_from_api(
            url_extension=self._url + "regional_data/",
            method="POST",
        )
        if meta_data_resp:
            return meta_data_resp.json()
        return None

    def _key(self, key: str) -> str:
        return getattr(self.KEYS, key)
