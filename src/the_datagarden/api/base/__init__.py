"""
Base module for The Data Garden API.

This module provides the foundation for interacting with The Data Garden API.
It includes the base class for API interactions and imports necessary
authentication components.

Classes:
    TheDataGardenAPI: Base class for interacting with The Data Garden API.

Imports:
    DatagardenEnvironment: Abstract base class for environment authentication.
    TheDatagardenProductionEnvironment: Concrete implementation of the production
                                                                        environment.
    URLExtension: Class for handling URL extensions.
"""

from collections import defaultdict
from typing import Iterator

import requests
from requests import Response

from the_datagarden.abc.api import BaseApi
from the_datagarden.abc.authentication import DatagardenEnvironment
from the_datagarden.api.authentication import AccessToken
from the_datagarden.api.authentication.environment import TheDatagardenProductionEnvironment
from the_datagarden.api.authentication.settings import (
    SHOW_REQ_DETAIL,
    DynamicEndpointCategories,
    URLExtension,
)
from the_datagarden.api.regions import Continent
from the_datagarden.api.regions.country import Country


class BaseDataGardenAPI(BaseApi):
    """
    Base class for interacting with The Data Garden API.
    """

    ACCESS_TOKEN: type[AccessToken] = AccessToken
    DYNAMIC_ENDPOINTS: dict = defaultdict(dict)

    def __init__(
        self,
        environment: type[DatagardenEnvironment] | None = None,
        email: str | None = None,
        password: str | None = None,
    ):
        self._environment = environment or TheDatagardenProductionEnvironment
        self._tokens = self.ACCESS_TOKEN(self._environment, email, password)
        self._base_url = self._environment().the_datagarden_url

    def _generate_url(self, url_extension: str) -> str:
        url = self._base_url + url_extension
        if url[-1] != "/":
            url += "/"
        return url

    def retrieve_from_api(
        self,
        url_extension: str,
        method: str = "GET",
        payload: dict | None = None,
        params: dict | None = None,
    ) -> Response | None:
        url = self._generate_url(url_extension)
        headers = self._tokens.header_with_access_token
        if SHOW_REQ_DETAIL:
            print(f"Request URL: {url}")
            print(f"Request headers: {headers}")
            print(f"Request method: {method}")
            print(f"Request payload: {payload}")
            print(f"Request params: {params}")
        match method:
            case "GET":
                response = requests.get(url, params=params, headers=headers)
            case "POST":
                response = requests.post(url, json=payload, headers=headers)
            case _:
                raise ValueError(f"Invalid method: {method}")

        return self._response_handler(response)

    def _response_handler(self, response: requests.Response) -> Response | None:
        if response.status_code == 200:
            return response
        else:
            response_dict = response.json()
            for k, v in response_dict.items():
                print(k)
                print(v)
            return None

    def _get_next_page(self, response: requests.Response) -> requests.Response | None:
        next_url = response.json().get("next")
        if not next_url:
            return None

        # Determine the original request method
        original_method = response.request.method

        headers = self._tokens.header_with_access_token

        if original_method == "GET":
            return requests.get(next_url, headers=headers)
        elif original_method == "POST":
            # For POST requests, we need to preserve the original payload
            original_payload = response.request.body
            return requests.post(next_url, data=original_payload, headers=headers)
        else:
            raise ValueError(f"Unsupported method for pagination: {original_method}")

    def _records_from_paginated_api_response(self, response: requests.Response | None) -> Iterator[dict]:
        while response:
            for record in response.json()["results"]:
                yield record
            response = self._get_next_page(response)

    def _create_url_extension(self, url_extensions: list[str]) -> str:
        url = "/".join(url_extensions).lower().replace(" ", "-")
        if url_extensions[-1] == "/":
            return url
        return url + "/"


class TheDataGardenAPI(BaseDataGardenAPI):
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        environment: type[DatagardenEnvironment] | None = None,
        email: str | None = None,
        password: str | None = None,
    ):
        if not self._initialized:
            super().__init__(environment, email, password)
            self._setup_continents()
            self._setup_countries()
            self.__class__._initialized = True

    def __getattr__(self, attr: str):
        for _, endpoints in self.DYNAMIC_ENDPOINTS.items():
            if attr.lower() in endpoints:
                return endpoints[attr.lower()]

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def world(self):
        response = self.retrieve_from_api(URLExtension.WORLD)
        return response.json()

    def continents(self, include_details: bool = False) -> list[str] | dict:
        continents = (
            self.DYNAMIC_ENDPOINTS.get(DynamicEndpointCategories.CONTINENTS, None) or self._setup_continents()
        )
        if not include_details:
            return continents.keys()
        return continents

    def countries(self, include_details: bool = False) -> list[str] | dict:
        countries = (
            self.DYNAMIC_ENDPOINTS.get(DynamicEndpointCategories.COUNTRIES, None) or self._setup_countries()
        )
        if not include_details:
            return countries.keys()
        return countries

    def _setup_continents(self):
        if not self.DYNAMIC_ENDPOINTS.get(DynamicEndpointCategories.CONTINENTS, None):
            continents = self.retrieve_from_api(URLExtension.CONTINENTS)
            for continent in self._records_from_paginated_api_response(continents):
                continent_method_name = continent["name"].lower().replace(" ", "_")
                self.DYNAMIC_ENDPOINTS[DynamicEndpointCategories.CONTINENTS].update(
                    {
                        continent_method_name: Continent(
                            url=self._create_url_extension([URLExtension.CONTINENT + continent["name"]]),
                            api=self,
                            name=continent["name"].lower(),
                        ),
                    }
                )

        return self.DYNAMIC_ENDPOINTS[DynamicEndpointCategories.CONTINENTS]

    def _setup_countries(self):
        if not self.DYNAMIC_ENDPOINTS.get(DynamicEndpointCategories.COUNTRIES, None):
            countries = self.retrieve_from_api(URLExtension.COUNTRIES)
            if not countries:
                return None
            for country in self._records_from_paginated_api_response(countries):
                country_method_name = country["name"].lower().replace(" ", "_")
                country_code = country["iso_cc_2"].lower()
                continent = country["parent_region"].lower()
                country = Country(
                    url=self._create_url_extension([URLExtension.COUNTRY + country["name"]]),
                    api=self,
                    name=country["name"],
                    continent=continent,
                )
                self.DYNAMIC_ENDPOINTS[DynamicEndpointCategories.COUNTRIES].update(
                    {
                        country_method_name: country,
                        country_code: country,
                    }
                )

        return self.DYNAMIC_ENDPOINTS[DynamicEndpointCategories.COUNTRIES]
