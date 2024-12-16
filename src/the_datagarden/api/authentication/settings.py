"""
Authentication settings for The DataGarden API.

This module contains constants and default values used for authentication
and API communication with The DataGarden service.

Constants:
    REQ_TOKEN_URL_EXTENSION (str): URL extension for requesting a token.
    REFRESH_TOKEN_URL_EXTENSION (str): URL extension for refreshing a token.
    HTTPS_PREFIX (str): Prefix for HTTPS URLs.
    BEARER_KEY (str): Prefix for Bearer token authentication.
    API_EXTENSION (str): Extension for API endpoints (currently empty).
    DEFAULT_HEADER (dict): Default headers for API requests.

"""

from decouple import config

from the_datagarden.version import __version__

INCLUDE_STATISTIC_PARAM = {"include_statistics": "y"}

STATISTICS_URL_EXTENSION = "statistics/"

SHOW_REQ_DETAIL = config("SHOW_REQ_DETAIL", default=False, cast=bool)
REQ_TOKEN_URL_EXTENSION = "user/token/"
REFRESH_TOKEN_URL_EXTENSION = "user/token/refresh/"

REGISTRATION_URL_EXTENSION = "user/enroll/"

HTTPS_PREFIX = "https://"
BEARER_KEY = "Bearer "
API_EXTENSION = ""

DEFAULT_HEADER: dict[str, str] = {
    "accept": "application/json",
    "accept-language": "en,nl-NL;q=0.9,nl;q=0.8,sv;q=0.7",
    "content-type": "application/json",
    "X-The-Datagarden-Version": "The_datagarden_pypi_package_version__" + __version__,
}


class URLExtension:
    WORLD = "world/"
    WORLD_DATA = "world/regional_data/"
    CONTINENTS = "continent/"
    CONTINENT = "continent/"
    COUNTRIES = "country/"
    COUNTRY = "country/"


class DynamicEndpointCategories:
    CONTINENTS = "continents"
    COUNTRIES = "countries"
