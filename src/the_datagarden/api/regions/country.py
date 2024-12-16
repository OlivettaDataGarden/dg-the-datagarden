from datagarden_models import CountryStats

from .base import Region
from .base.settings import CountryKeys


class Country(Region):
    KEYS = CountryKeys
    REGION_STATS_MODEL = CountryStats
