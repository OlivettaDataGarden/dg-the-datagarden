================
Continent Object
================

The Continent object
--------------------
The continent object provides methods to get public data for a continent or its direct subregions (i.e. the countries).
A countint object can simply be retrieved from TheDataGardenAPI object by calling the continent name:

.. code-block:: python

    # Retrieving the continent object for Europe from The DataGarden API
    >>> from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> europe = my_datagarden_api.europe
    >>> print(europe)
    >>> print(type(europe))

.. code-block:: console

    Continent : Europe
    <class 'the_datagarden.api.regions.continent.Continent'>


The continent's meta data
-------------------------
To find out more about a continent's sub regional structure as well as what data is available for a continent you can
fetch a meta data object from the continent. The ``europe_meta_data`` object below can be used to get an overview of available region types.

.. code-block:: python

    # Retrieving the meta data for Europe and the available region types
    >>> europe = my_datagarden_api.europe
    >>> europe_meta_data = europe.meta_data
    >>> print(europe_meta_data.region_types)

For the continent object only the continent and country region types are available. For subregions within the countries you need to go
to the country object.

.. code-block:: console

    ['continent', 'country']

To get an overview of which data models are available for a continent object and its subregions (i.e. the countries), you can call
the `available_model_names`  method on the TheDataGardenAPI continent object:

.. code-block:: python

    # Retrieving available data models for Europe
    >>> europe = my_datagarden_api.europe
    >>> europe_meta_data = europe.meta_data
    >>> print(europe_meta_data.continent.regional_data_models) # will only show data models available for continent
    >>> print(europe_meta_data.country.regional_data_models) # will show data models available for all countries in continent

You can get more specific information for a specific data model on regional level.

.. code-block:: python

    # Retrieving the detailed information for the economics data model for Europe
    >>> europe = my_datagarden_api.europe
    >>> continent_only_meta_data = europe.meta_data.continent
    >>> economics_meta_data = continent_only_meta_data.economics
    >>> print(economics_meta_data.source_names)
    ['UNCTAD']
    >>> print(economics_meta_data.period_types)
    ['Y']
    >>> print(economics_meta_data.from_period)
    '1970-01-01T00:00:00Z'
    >>> print(economics_meta_data.to_period)
    '2023-01-01T00:00:00Z'

The economics data model for Europe is available from the UNCTAD source and is available from 1970 to up to and including 2023
and has Yearly datapoints.


Populating a data model with data
---------------------------------
Now that we can see what data models are available, you can retrieve the datamodel
by calling the data model name on the continent object:

.. code-block:: python

    # Retrieving demographic data for Europe
    >>> europe = my_datagarden_api.europe
    >>> europe_demographics = europe.demographics
    >>> print(type(europe_demographics))
    >>> print(europe_demographics)

The demographics attribute is in fact an object of type TheDataGardenRegionalDataModel.
By printing the object you can see what type of records as well as the number of
records that it contains. By default there are no records in the object:

.. code-block:: console

    <class 'the_datagarden.models.regional_data_model.TheDataGardenRegionalDataModel'>
    TheDataGardenRegionalDataModel : Demographics : (count=0)


When you call the demographics object (ie. when you call the TheDataGardenRegionalDataModel),
it automatically fetches data from The DataGarden API.
If you don't specify any query parameters, it will return the API's default dataset.
For details about these default values, please refer to https://www.the-datagarden.io/api-docs.

.. code-block:: python

    # Calling the germany demographics attribute without query parameters
    # will populate the object (europe_demographics) with the default dataset from The DataGarden API
    >>> europe = my_datagarden_api.europe
    >>> europe_demographics = europe.demographics
    >>> europe_demographics()
    >>> print(europe_demographics)

As you can see, in this example de demographic attribute now contains 9 records:

.. code-block:: console

    TheDataGardenRegionalDataModel : Demographics : (count=3)

Adding query parameters is easy, in this example we will retrieve data from 2010 to 2025:

.. code-block:: python

    # Calling the germany demographics attribute with query parameters
    >>> europe = my_datagarden_api.europe
    >>> europe_demographics = europe.demographics
    >>> europe_demographics(period_from="2010-01-01", period_to="2024-01-01")
    >>> print(europe_demographics)

Now the demographic attribute contains 15 records.

.. code-block:: console

    TheDataGardenRegionalDataModel : Demographics : (count=15)

The counter in the result above represents the number of RegionalDataRecords retrieved by the TheDataGardenRegionalDataModel
based upon the queries from the user. Each RegionalDataRecord represents a distinct data point for the datamodel's
source, period, and period type. So for example for the yearly data you will find max 1 record per year per data source.

For more details please see the :doc:`regional_data_model` documentation.

Converting to DataFrames
------------------------
To view your data in a tabular format, you can easily convert it to either a Polars or Pandas dataframe:

.. code-block:: python

    >>> europe = my_datagarden_api.europe
    >>> europe_demographics = europe.demographics
    >>> europe_demographics(period_from="2010-01-01", period_to="2024-01-01")
    >>> europe_df = europe_demographics.to_polars()  # or europe_demographics.to_pandas()
    >>> print(europe_df.head())
    >>> print(europe_df.columns)


.. code-block:: console

    ┌────────┬─────────────┬────────────────┬──────────┬───┬────────────────┬──────────────────────┬─────────────┬──────────────┐
    │ name   ┆ region_type ┆ un_region_code ┆ iso_cc_2 ┆ … ┆ source_name    ┆ period               ┆ period_type ┆ data_type    │
    │ ---    ┆ ---         ┆ ---            ┆ ---      ┆   ┆ ---            ┆ ---                  ┆ ---         ┆ ---          │
    │ str    ┆ str         ┆ str            ┆ str      ┆   ┆ str            ┆ str                  ┆ str         ┆ str          │
    ╞════════╪═════════════╪════════════════╪══════════╪═══╪════════════════╪══════════════════════╪═════════════╪══════════════╡
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2010-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2011-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2012-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2013-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2014-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    └────────┴─────────────┴────────────────┴──────────┴───┴────────────────┴──────────────────────┴─────────────┴──────────────┘
    ['name', 'region_type', 'un_region_code', 'iso_cc_2', 'local_region_code', 'local_region_code_type', 'parent_region_code',
     'parent_region_code_type', 'parent_region_type', 'region_level', 'source_name', 'period', 'period_type', 'data_model_name']


Notice that europe_df.columns does not contain any columns for the actual demographics data.
This is because the to_polars() method only adds specified data columns by default.
To see the complete data in the dataframe, use the full_models_to_polars() method instead.
This will add a fully flattened version of the Demographics data model to the dataframe.
For more options to control what data is added to the dataframe, see the :doc:`regional_data_model` page.

Both methods are also available as pandas methods (`to_pandas()` and `full_models_to_pandas()`).
