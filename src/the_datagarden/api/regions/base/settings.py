from enum import StrEnum


class ResponseKeys(StrEnum):
    AVAILABLE_MODELS = "AVAILABLE_MODELS"
    STATISTICS = "STATISTICS"


class RegionKeys(StrEnum): ...


class ContinentKeys(RegionKeys):
    AVAILABLE_MODELS = "available_data_on_continent_level"
    STATISTICS = "statistics"


class CountryKeys(RegionKeys):
    AVAILABLE_MODELS = "models_per_region_level"
    STATISTICS = "statistics"
