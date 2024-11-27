from enum import StrEnum


class ResponseKeys(StrEnum):
    AVAILABLE_MODELS = "AVAILABLE_MODELS"
    STATISTICS = "STATISTICS"


class RegionKeys(StrEnum): ...


class ContinentKeys(RegionKeys):
    AVAILABLE_MODELS = "available_data_on_continent_level"
    STATISTICS = "continent_statistics"


class CountryKeys(RegionKeys):
    AVAILABLE_MODELS = "available_data_on_country_level"
    STATISTICS = "country_statistics"
