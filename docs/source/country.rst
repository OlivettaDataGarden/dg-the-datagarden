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

    The country object is an instance of the Country class represented by the Country name.

.. code-block:: console

    Region Germany
    <class 'the_datagarden.api.regions.country.Country'>


Checking available data models
------------------------------
To get an overview of which data models are available for a country object, you can call
the `available_model_names` method on the country object:

.. code-block:: python

    # Retrieving available data models for Germany
    >>> from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> germany = my_datagarden_api.germany
    >>> print(germany.available_model_names)

.. code-block:: console

    ['Health', 'Economics', 'Demographics']

This method returns a list of available data models.

If you want to get more information about the available datamodels, you can call the `available_models` method:

.. code-block:: python

    # Retrieving detailed information about the available data models
    >>> germany = my_datagarden_api.germany
    >>> print(germany.available_models)

This returns a dictionary with the data model names as keys and their metadata as values:

.. code-block:: json

    {
        "Health": {
            "count": 35,
            "sources": ["UNICEF", "Eurostat"],
            "to_period": "2023-01-01T00:00:00Z",
            "from_period": "2000-01-01T00:00:00Z",
            "period_type": ["Y"]
        },
        "Economics": "{...}",
        "Demographics": "{...}"
    }

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

As you can see, in this examople de demographic attribute now contains 9 records:

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
    >>> germany_df = germany.to_polars()  # or germany.to_pandas()
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

Just like with the continents the germany_df.columns does not contain any columns for the actual demographics data.
Please check the :doc:`regional_data_model` documentation for more details on how to added the actual model data to the dataframe.
Note that the source name now contains source names like "Eurostat" and "United Nations", indicating that demographics data
for germany is available from multiple sources.
Also on country level you can see the complete data in the dataframe by using full_models_to_polars() method (or full_models_to_pandas()).
