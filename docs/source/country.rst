==============
Country Object
==============

The Country object
------------------
The DataGardenApi will return a Country object by calling the country name on the api object.

.. code-block:: python

    # Retrieving the country object for Germany from The DataGarden API
    >>> from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> germany = my_datagarden_api.germany
    >>> print(germany)
    >>> print(type(germany))

The object ``germany`` is an instance of the class ``Country`` represented by the Country name.

.. code-block:: console

    Region Germany
    <class 'the_datagarden.api.regions.country.Country'>


The country's meta data
-----------------------

To find out more about a country's sub regional structure as well as what data is available for a country you can
fetch a meta data object from the country. The ``german_meta_data`` object below can be used to get an overview of available region types.

.. code-block:: python

    # Retrieving the meta data for Germany and the available region types
    >>> germany = my_datagarden_api.germany
    >>> german_meta_data = germany.meta_data
    >>> print(german_meta_data.region_types)

The region types will be returned in order of their hierarchy. Region type hierarchy usually follows the country's administrative structure.

.. code-block:: console

    ['country', 'state', 'region', 'district', 'city']

Be aware that not (yet) all countries in the DataGarden are populated with subregions

The meta data object also contains an overview of available data Models for the country.

.. code-block:: python

    # Retrieving the available data models for Germany
    >>> germany = my_datagarden_api.germany
    >>> german_meta_data = germany.meta_data
    >>> print(german_meta_data.regional_data_models)

This will return a list of available regional data models for all of Germany.

.. code-block:: console

    ['health', 'demographics', 'economics', 'weather']

Each model in this list is available for at least one of the region types in the country but usually more.
Some models are deliberately not available for all region types. The Weather model for example
doesn't have value for very big regions like the United States nor does it make sense to store them on
zip code level. Finding out which models are available for a specific region type is easy.

.. code-block:: python

    # Retrieving the available data models for Germany
    >>> germany = my_datagarden_api.germany
    >>> district_meta_data = germany.meta_data.district
    >>> print(district_meta_data.regional_data_models)

Just retrieve the meta data object for the region type you are interested in and call the `regional_data_models` attribute.
In this example we retrieve the available regional data models for the german district region type and we see that the
health model is not available for this region type although it is available for some region_types of the country.

.. code-block:: console

    ['demographics', 'economics']

The country itself is also a region type. So you can retrieve the available data models on level of the country as well.

.. code-block:: python

    # Retrieving the available data models for Germany
    >>> germany = my_datagarden_api.germany
    >>> country_only_meta_data = germany.meta_data.country
    # meta data for country level only
    >>> print(country_only_meta_data.regional_data_models)
    ['health', 'demographics', 'economics']
    # meta data for al region types in the country
    >>> german_meta_data = germany.meta_data
    >>> print(german_meta_data.regional_data_models)
    ['health', 'demographics', 'economics', 'weather']


You can get more specific information for a specific data model on regional level.

.. code-block:: python

    # Retrieving the available data models for Germany
    >>> germany = my_datagarden_api.germany
    >>> country_only_meta_data = germany.meta_data.country
    >>> economics_meta_data = country_only_meta_data.economics
    >>> print(economics_meta_data.source_names)
    ['UNCTAD', 'Eurostat']
    >>> print(economics_meta_data.period_types)
    ['Y']
    >>> print(economics_meta_data.from_period)
    '1975-01-01T00:00:00Z'
    >>> print(economics_meta_data.to_period)
    '2023-01-01T00:00:00Z'

For the country germany there is economics data available from the UNCTAD and Eurostat sources.
There is only yearly data available ranging from 1975 to up to and including 2023.


Populating a data model with data
---------------------------------
Now that we can see what data models are available, you can retrieve the datamodel
by calling the data model name on the country object:

.. code-block:: python

    # Retrieving demographic data for Germany
    >>> germany = my_datagarden_api.germany
    >>> germany_demographics = germany.demographics
    >>> print(type(germany_demographics))
    >>> print(germany_demographics)

The demographics attribute is in fact an object of type TheDataGardenRegionalDataModel.
By printing the object you can see what type of records as well as the number of
records that it contains. By default there are no records in the object:

.. code-block:: console

    <class 'the_datagarden.models.regional_data_model.TheDataGardenRegionalDataModel'>
    TheDataGardenRegionalDataModel : Demographics : (count=0)

Adding data records to the data model
-------------------------------------
When you call the demographics object (ie. when you call the TheDataGardenRegionalDataModel),
it automatically fetches data from The DataGarden API.
If you don't specify any query parameters, it will return the API's default dataset.
For details about these default values, please refer to https://www.the-datagarden.io/api-docs.

.. code-block:: python

    # Calling the germany demographics attribute without query parameters
    # will populate the object with the default dataset from The DataGarden API
    >>> germany = my_datagarden_api.germany
    >>> germany_demographics = germany.demographics
    >>> germany_demographics()
    >>> print(germany_demographics)

As you can see, in this example de demographic attribute now contains 9 records:

.. code-block:: console

    TheDataGardenRegionalDataModel : Demographics : (count=9)

Adding query parameters is easy, in this example we will retrieve data from 2010 to 2025:

.. code-block:: python

    # Calling the germany demographics attribute with query parameters
    >>> germany = my_datagarden_api.germany
    >>> germany_demographics = germany.demographics
    >>> germany_demographics(from_date="2010-01-01", to_date="2025-01-01")
    >>> print(germany_demographics)

Now the demographic attribute contains 30 records.

.. code-block:: console

    TheDataGardenRegionalDataModel : Demographics : (count=30)

Regional Data Model Records
---------------------------
A TheDataGardenRegionalDataModel instance contains a collection of unique RegionalDataRecord objects.
Each RegionalDataRecord represents a distinct data point defined by among others its source, time period, and period type
(e.g., yearly, monthly). As these are unique data points they will only be added once.
Running germany_demographics() multiple times will not create duplicate records.

For more details on how uniqueness is determined and how to work with TheDataGardenRegionalDataModel objects,
please see the :doc:`regional_data_model` documentation.

Converting to DataFrames
------------------------
To view your data in a tabular format, you can easily convert it to either a Polars or Pandas dataframe:

.. code-block:: python

    >>> germany = my_datagarden_api.germany
    >>> germany_demographics = germany.demographics
    >>> germany_demographics()
    >>> germany_df = germany_demographics.to_polars()  # or germany_demographics.to_pandas()
    >>> print(germany_df.head())
    >>> print(germany_df.columns)

.. code-block:: console

    ┌─────────┬─────────────┬────────────────┬──────────┬───┬────────────────┬──────────────────────┬─────────────┬────────────────┐
    │ name    ┆ region_type ┆ un_region_code ┆ iso_cc_2 ┆ … ┆ source_name    ┆ period               ┆ period_type ┆ data_model_name│
    │ ---     ┆ ---         ┆ ---            ┆ ---      ┆   ┆ ---            ┆ ---                  ┆ ---         ┆ ---            │
    │ str     ┆ str         ┆ str            ┆ str      ┆   ┆ str            ┆ str                  ┆ str         ┆ str            │
    ╞═════════╪═════════════╪════════════════╪══════════╪═══╪════════════════╪══════════════════════╪═════════════╪════════════════╡
    │ Germany ┆ country     ┆ 276            ┆ DE       ┆ … ┆ Eurostat       ┆ 2010-01-01T00:00:00Z ┆ Y           ┆ Demographics   │
    │ Germany ┆ country     ┆ 276            ┆ DE       ┆ … ┆ United Nations ┆ 2010-01-01T00:00:00Z ┆ Y           ┆ Demographics   │
    │ Germany ┆ country     ┆ 276            ┆ DE       ┆ … ┆ United Nations ┆ 2011-01-01T00:00:00Z ┆ Y           ┆ Demographics   │
    │ Germany ┆ country     ┆ 276            ┆ DE       ┆ … ┆ Eurostat       ┆ 2011-01-01T00:00:00Z ┆ Y           ┆ Demographics   │
    │ Germany ┆ country     ┆ 276            ┆ DE       ┆ … ┆ Eurostat       ┆ 2012-01-01T00:00:00Z ┆ Y           ┆ Demographics   │
    └─────────┴─────────────┴────────────────┴──────────┴───┴────────────────┴──────────────────────┴─────────────┴────────────────┘
    ['name', 'region_type', 'un_region_code', 'iso_cc_2', 'local_region_code', 'local_region_code_type', 'parent_region_code',
    'parent_region_code_type', 'parent_region_type', 'region_level', 'source_name', 'period', 'period_type', 'data_model_name']

As you can see the to_polars() method without parameters returns a dataframe that does not contain any columns for the actual demographics data.
Please check the :doc:`regional_data_model` documentation for more details on how to added the actual model data to the dataframe.
You can add all data from the data model to the dataframe by using the full_models_to_polars() method (or full_models_to_pandas())
(all data will be flattened though resulting in a dataframe with a lot of columns)

Note that the source name now contains source names like "Eurostat" and "United Nations", indicating that demographics data
for germany is available from multiple sources.
