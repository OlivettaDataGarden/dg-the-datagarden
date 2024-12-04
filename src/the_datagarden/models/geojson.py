from typing import Any

import pandas as pd
import polars as pl
from pydantic import BaseModel

from the_datagarden.api.base import BaseApi

GEJSON_UNIQUE_FIELDS = [
    "region_type",
    "iso_cc_2",
    "local_region_code",
    "local_region_code_type",
    "region_level",
]


class Properties(BaseModel):
    name: str
    region_level: int
    region_type: str
    iso_cc_2: str
    local_region_code: str
    local_region_code_type: str


class Geometry(BaseModel):
    type: str
    coordinates: list


class Feature(BaseModel):
    type: str = "Feature"
    properties: Properties
    geometry: Geometry


class RegionGeoJSONDataRecord(BaseModel):
    name: str | None = None
    region_type: str | None = None
    iso_cc_2: str | None = None
    local_region_code: str | None = None
    local_region_code_type: str | None = None
    region_level: int = 0
    feature: Feature

    def record_hash(self) -> str:
        hash_str = ".".join([str(getattr(self, key)) for key in sorted(GEJSON_UNIQUE_FIELDS)])
        return str(hash(hash_str))

    def __str__(self):
        return f"RegionGeoJSONDataRecord: {self.name} ({self.region_type} for {self.local_region_code})"


class TheDataGardenRegionGeoJSONModel:
    """
    Model to hold response data from the The Data Garden API Region GeoJSON endpoint.

    The model hold a list of regional_data records containg a regional data model
    for the region for a specific set op sources, periods and period types.

    The data can be converted to Polars and Pandas dataframes by the following
    methods:
    - to_polars(model_convertors: dict | None = None) -> pl.DataFrame
        model_convertors dict will be used to covert specifc model fields to dataframe
        columns.
    - full_model_to_polars() -> pl.DataFrame

    For pandas dataframes you can use the same methods:
    - to_pandas(model_convertors: dict | None = None) -> pd.DataFrame
    - full_model_to_pandas() -> pd.DataFrame
    """

    def __init__(self, api: "BaseApi", region_url: str):
        self._api: BaseApi = api
        self._region_url: str = region_url
        self._levels_requested: list[int] = []
        self._geojson_records: dict[str, RegionGeoJSONDataRecord] = {}

    def __str__(self):
        return f"TheDataGardenRegionGeoJSONModel : GeoJSON : (count={len(self._geojson_records)})"

    def __repr__(self):
        return self.__str__()

    def __call__(self, region_level: int = 0) -> "TheDataGardenRegionGeoJSONModel":
        if region_level not in self._levels_requested:
            features = self.geojson_paginated_data_from_api(region_level=region_level)
            if features:
                self.set_items(features)
                self._levels_requested.append(region_level)
        return self

    def _response_has_next_page(self, model_data_resp: dict) -> bool:
        pagination = model_data_resp.get("pagination", None)
        if not pagination:
            return False
        return pagination.get("next_page", None) is not None

    def _next_page_pagination(self, model_data_resp: dict) -> dict | None:
        pagination = model_data_resp.pop("pagination", None)
        if not pagination:
            return None
        next_page = pagination.get("next_page", None)
        if not next_page:
            return None
        return {"page": next_page}

    def geojson_paginated_data_from_api(self, region_level: int):
        geojson_data_resp = self.geojson_data_from_api(region_level=region_level)
        while geojson_data_resp and self._response_has_next_page(geojson_data_resp):
            next_page_pagination = self._next_page_pagination(geojson_data_resp)
            if next_page_pagination:
                next_page_resp = self.geojson_data_from_api(
                    pagination=next_page_pagination, region_level=region_level
                )
                if next_page_resp:
                    geojson_data_resp["features"].extend(next_page_resp["features"])
                    geojson_data_resp["pagination"] = next_page_resp["pagination"]

        return geojson_data_resp

    def geojson_data_from_api(
        self, region_level: int, pagination: dict[str, str] | None = None
    ) -> dict | None:
        payload: dict[str, Any] = {"region_level": region_level}
        if pagination:
            payload = payload | {"pagination": pagination}
        geojson_data_resp = self._api.retrieve_from_api(
            url_extension=self._region_url + "geojson/",
            method="POST",
            payload=payload,
        )
        if geojson_data_resp:
            return geojson_data_resp.json()
        return None

    def set_items(self, data: dict):
        for feature in data["features"]:
            feature = Feature(**feature)
            data_record_items = {
                "name": feature.properties.name,
                "region_type": feature.properties.region_type,
                "iso_cc_2": feature.properties.iso_cc_2,
                "local_region_code": feature.properties.local_region_code,
                "local_region_code_type": feature.properties.local_region_code_type,
                "region_level": feature.properties.region_level,
                "feature": feature,
            }
            data_record = RegionGeoJSONDataRecord(**data_record_items)
            self._geojson_records.update({data_record.record_hash(): data_record})

    def to_polars(self) -> pl.DataFrame:
        """
        Convert the data to a polars dataframe using a dictionary of model attributes to convert to columns
        """
        converted_records = []
        for record in self._geojson_records.values():
            record_dict = record.model_dump()
            converted_records.append(record_dict)
        return pl.from_records(converted_records)

    def to_pandas(self) -> pd.DataFrame:
        """
        Convert the data to a pandas dataframe
        """
        return self.to_polars().to_pandas()

    def __iter__(self):
        """Makes the class iterable over the values in _data_records"""
        return iter(self._geojson_records.values())

    def __len__(self):
        """Returns the number of records"""
        return len(self._geojson_records)

    @property
    def geojson_records(self) -> list[RegionGeoJSONDataRecord]:
        return list(self._geojson_records.values())
