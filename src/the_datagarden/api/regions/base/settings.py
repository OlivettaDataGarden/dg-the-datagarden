from enum import StrEnum


class ResponseKeys(StrEnum):
    AVAILABLE_MODELS = "AVAILABLE_MODELS"


class RegionKeys(StrEnum): ...


class ContinentKeys(RegionKeys):
    AVAILABLE_MODELS = "available_data_on_continent_level"


class CountryKeys(RegionKeys):
    AVAILABLE_MODELS = "available_data_on_country_level"
