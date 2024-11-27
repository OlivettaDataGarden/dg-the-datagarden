================
Continent Object
================
The continent object provides methods to get data on a continent or to access to subregion (countries) objects from the continent.

To get an overview of what data is available in the continent object, you can call the continents method from the TheDataGardenAPI object:

.. code-block:: python

    # Retrieving continents list for The Data Garden API
    >>> from from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> europe = my_datagarden_api.europe
    >>> print(europe.available_models())

.. code-block:: console

    dict_keys(['Economics', 'Demographics'])

The continents method simply returns a list of available continents. You can directly acccess the continent objects in two ways. First by calling the continents method with the include_details flag:

.. code-block:: python

    # Retrieving continent objects from The Data Garden API
    >>> from from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> europe = my_datagarden_api.europe
    >>> print(europe.available_models(include_details=True))


This returns a dictionary with the continent names as keys and the continent objects as values:

.. code-block:: console

    {'Economics': {'count': 19, 'sources': ['UNCTAD'], 'to_period': '2023-01-01T00:00:00Z', 'from_period': '2005-01-01T00:00:00Z', 'period_type': ['Y']}, 'Demographics': {'count': 151, 'sources': ['United Nations'], 'to_period': '2100-01-01T00:00:00Z', 'from_period': '1950-01-01T00:00:00Z', 'period_type': ['Y']}}
