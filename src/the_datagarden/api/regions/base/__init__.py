from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from the_datagarden.api.authentication.settings import INCLUDE_STATISTIC_PARAM
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

    _info: dict = {}
    _available_models: dict = {}
    _model_data_storage: dict[str, TheDataGardenRegionalDataModel] = {}

    KEYS: type[StrEnum]

    def __repr__(self):
        return f"Region {self.info.get('name', '')}"

    def __init__(self, url: str, api: BaseApi):
        self._region_url = url
        self._api = api
        self._geojsons = TheDataGardenRegionGeoJSONModel(api=api, region_url=url)

    def __getattr__(self, attr: str):
        if attr in self._api_model_names:
            return self._model_data_from_storage(model_name=attr)
        if attr == "geojsons":
            return self._geojsons

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def _model_data_from_storage(self, model_name: str) -> TheDataGardenRegionalDataModel | None:
        stored_model_data = self._model_data_storage.get(model_name, None)
        if not stored_model_data:
            self._model_data_storage[model_name] = TheDataGardenRegionalDataModel(
                model_name=model_name, api=self._api, region_url=self._region_url
            )
            return self._model_data_storage[model_name]

        return stored_model_data

    @property
    def info(self) -> dict | None:
        """
        Get the region info from the API.
        """
        if not self._info:
            info_resp = self._api.retrieve_from_api(
                url_extension=self._region_url,
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

    @property
    def available_model_names(self) -> list[str]:
        if not self._available_models:
            self._set_available_models()
        return list(self._available_models.keys())

    @property
    def available_models(self) -> set:
        if not self._available_models:
            self._set_available_models()

        return {item for models_per_level in self._available_models.values() for item in models_per_level}

    @property
    def _api_model_names(self) -> list[str]:
        return [model.lower() for model in self.available_models]

    def _set_available_models(self) -> None:
        if self._available_models:
            return

        if self.statistics:
            self._available_models = self._info.get(self._key(ResponseKeys.AVAILABLE_MODELS), [])
        return

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
