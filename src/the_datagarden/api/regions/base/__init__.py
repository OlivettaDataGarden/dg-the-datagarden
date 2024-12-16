from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from the_datagarden.api.authentication.settings import STATISTICS_URL_EXTENSION
from the_datagarden.api.base import BaseApi
from the_datagarden.models import TheDataGardenRegionalDataModel, TheDataGardenRegionGeoJSONModel

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

    REGION_STATS_MODEL: type[BaseModel]
    _region_stats: BaseModel | None = None

    KEYS: type[StrEnum]

    def __repr__(self):
        return f"{self.__class__.__name__} : {self._name}"

    def __init__(self, url: str, api: BaseApi, name: str, continent: str | None = None):
        self._region_url = url
        self._api = api
        self._available_models: dict = {}
        self._model_data_storage: dict[str, TheDataGardenRegionalDataModel] = {}
        self._geojsons = TheDataGardenRegionGeoJSONModel(api=api, region_url=url)
        self._name = name
        self._continent = continent

    def __getattr__(self, attr: str):
        if attr in self.available_model_names:
            return self._model_data_from_storage(model_name=attr)
        if attr == "geojsons":
            return self._geojsons

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def _model_data_from_storage(self, model_name: str) -> TheDataGardenRegionalDataModel | None:
        stored_model_data = self._model_data_storage.get(model_name, None)
        if not stored_model_data:
            self._model_data_storage[model_name] = TheDataGardenRegionalDataModel(
                model_name=model_name, api=self._api, region_url=self._region_url, meta_data=self.meta_data
            )
            return self._model_data_storage[model_name]

        return stored_model_data

    @property
    def meta_data(self) -> BaseModel | None:
        """
        Get the region statistics info from the API.
        """
        if not self._region_stats:
            region_stats_resp = self._api.retrieve_from_api(
                url_extension=self._region_url + STATISTICS_URL_EXTENSION,
            )
            if region_stats_resp and region_stats_resp.status_code == 200:
                region_stats_resp_json = region_stats_resp.json().get(self._key(ResponseKeys.STATISTICS), {})
                self._region_stats = self.REGION_STATS_MODEL(
                    region_stats_resp_json if isinstance(region_stats_resp_json, dict) else {}
                )

        return self._region_stats

    @property
    def region_types(self) -> list[str]:
        if not self.meta_data:
            return []
        return self.meta_data.region_types

    @property
    def available_model_names(self) -> list[str]:
        if not self.meta_data:
            return []
        return self.meta_data.regional_data_models

    def _key(self, key: str) -> str:
        return getattr(self.KEYS, key)
