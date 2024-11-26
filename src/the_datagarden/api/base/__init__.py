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

from the_datagarden.abc.api import BaseApi
from the_datagarden.abc.authentication import DatagardenEnvironment
from the_datagarden.api.authentication import AccessToken
from the_datagarden.api.authentication.environment import (
    TheDatagardenProductionEnvironment,
)
from the_datagarden.api.authentication.settings import (
    DynamicEndpointCategories,
    URLExtension,
)
from the_datagarden.api.regions import Continent


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
    ):
        url = self._generate_url(url_extension)
        headers = self._tokens.header_with_access_token
        match method:
            case "GET":
                return requests.get(url, params=params, headers=headers)
            case "POST":
                return requests.post(url, json=payload, headers=headers)
            case _:
                raise ValueError(f"Invalid method: {method}")

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
    def __init__(
        self,
        environment: type[DatagardenEnvironment] | None = None,
        email: str | None = None,
        password: str | None = None,
    ):
        super().__init__(environment, email, password)
        self.continents()
        self.country()

    def __getattr__(self, attr: str):
        for _, endpoints in self.DYNAMIC_ENDPOINTS.items():
            if attr in endpoints:
                return endpoints[attr]

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def world(self):
        response = self.retrieve_from_api(URLExtension.WORLD)
        return response.json()

    def continents(self):
        if not self.DYNAMIC_ENDPOINTS.get(DynamicEndpointCategories.CONTINENTS, None):
            continents = self.retrieve_from_api(URLExtension.CONTINENTS)
            for continent in self._records_from_paginated_api_response(continents):
                continent_method_name = continent["name"].lower().replace(" ", "_")
                self.DYNAMIC_ENDPOINTS[DynamicEndpointCategories.CONTINENTS].update(
                    {
                        continent_method_name: Continent(
                            url=self._create_url_extension([URLExtension.CONTINENT + continent["name"]]),
                            api=self,
                        ),
                    }
                )

        return self.DYNAMIC_ENDPOINTS[DynamicEndpointCategories.CONTINENTS]

    def country(self):
        if not self.DYNAMIC_ENDPOINTS.get(DynamicEndpointCategories.COUNTRIES, None):
            countries = self.retrieve_from_api(URLExtension.COUNTRIES)
            for country in self._records_from_paginated_api_response(countries):
                country_method_name = country["name"].lower().replace(" ", "_")
                self.DYNAMIC_ENDPOINTS[DynamicEndpointCategories.COUNTRIES].update(
                    {
                        country_method_name: self._create_url_extension(
                            [URLExtension.COUNTRY + country["name"]]
                        ),
                    }
                )

        return self.DYNAMIC_ENDPOINTS[DynamicEndpointCategories.COUNTRIES]
