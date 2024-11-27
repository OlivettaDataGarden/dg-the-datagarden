================
TheDataGardenAPI
================
Once your account is set up, you can initialize the TheDataGardenAPI object. In all the examples below it is assumed that email and password are defined in the .env file:


Continents
----------


.. code-block:: python

    # Retrieving continents list for The Data Garden API
    >>> from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> my_datagarden_api.continents()

.. code-block:: console

    dict_keys(['africa', 'asia', 'europe', 'latin_america_and_the_caribbean', 'northern_america', 'oceania'])

The continents method simply returns a list of available continents. You can directly access the continent objects in two ways. First by calling the continents method with the include_details flag:

.. code-block:: python

    # Retrieving continent objects from The Data Garden API
    >>> from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> my_datagarden_api.continents(include_details=True)

This returns a dictionary with the continent names as keys and the continent objects as values:

.. code-block:: console

    {'africa': <the_datagarden.api.regions.continent.Continent object at ...>, 'asia': <the_datagarden.api.regions.continent.Continent object at ...>, 'europe': etc.}


And the second way is by directly calling a continent object from the TheDataGardenAPI:

.. code-block:: python

    # Retrieving continent objects from The Data Garden API
    >>> from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> my_datagarden_api.africa

This returns only the africa continent object:

.. code-block:: console

    <the_datagarden.api.regions.continent.Continent object at ....>


A wide variety of methods are available for the continent objects. These can be found in the :doc:`continent` section.


.. code-block:: python

    # initialize the TheDataGardenAPI instance
    >>> from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()

.. code-block:: console

    Initializing : TheDatagardenProductionEnvironment
