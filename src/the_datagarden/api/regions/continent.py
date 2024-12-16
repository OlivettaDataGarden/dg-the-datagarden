from datagarden_models import ContinentStats

from .base import Region
from .base.settings import ContinentKeys


class Continent(Region):
    KEYS = ContinentKeys
    REGION_STATS_MODEL = ContinentStats
