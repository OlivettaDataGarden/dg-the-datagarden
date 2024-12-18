==================
the-datagarden SDK
==================

The-datagarden package is a Python SDK built on top of The-DataGarden API. The SDK provides easy access to continent and country regional hierarchies,
as well as public data related to these regions. All data from The-DataGarden API is stored in normalized datamodels like ``Demographics``, ``Health``
or ``Economics``. This allows you as a data professional to create value from this data without having to worry about the (varying) data structure and
api's from the sources.

Additionally, The-DataGarden API also provides country and regional GeoJSONs. The SDK makes is easy for you to combine public data abd you own data and merge them into
geosjon Feature collections, making geographic visualisation easy.


The-DataGarden SDK main use case
--------------------------------
The SDK is designed to make it easy to access and work with the DataGarden data. After initializing the SDK you simply
retrieve data for a specific continent, country or subregion by calling the appropriate datamodel.

.. code-block:: python

    # initialize a country object and retrieve the demographics attribute
    >>> nl = the_datagarden_api.netherlands # or nl = the_datagarden_api.NL
    >>> nl_demographics = nl.demographics()
    TheDataGardenRegionalDataModel : Demographics : (count=5)

In this example the `nl_demographics` object holds 5 records. Each record contains demographic data for the Netherlands for a specific
period and period type combination. The data can be made accessible in a tabular format by converting the object to a pandas or polars dataframe.

.. code-block:: python

    # convert demographics data to a polars dataframe
    >>> dataframe = nl_demographics.full_model_to_polars()
    >>> print(dataframe["period", "source_name", "data_model_name", "population.total", "population.total_male", "population.total_female"])

.. code-block:: text

    ┌───────────────┬────────────┬─────────────────┬──────────────────┬───────────────────────┬─────────────────────────┐
    │ period        ┆ source_name┆ data_model_name ┆ population.total ┆ population.total_male ┆ population.total_female │
    │ ---           ┆ ---        ┆ ---             ┆ ---              ┆ ---                   ┆ ---                     │
    │ str           ┆ str        ┆ str             ┆ f64              ┆ f64                   ┆ f64                     │
    ╞═══════════════╪════════════╪═════════════════╪══════════════════╪═══════════════════════╪═════════════════════════╡
    │ 2022-01-01T0Z ┆ Eurostat   ┆ Demographics    ┆ null             ┆ 8.745468e6            ┆ 8.845204e6              │
    │ 2022-01-01T0Z ┆ United Nat ┆ Demographics    ┆ 1.7789347e7      ┆ 8.890013e6            ┆ 9.014408e6              │
    │ 2023-01-01T0Z ┆ Eurostat   ┆ Demographics    ┆ null             ┆ 8.850309e6            ┆ 8.960982e6              │
    │ 2023-01-01T0Z ┆ United Nat ┆ Demographics    ┆ 1.8019495e7      ┆ 8.986255e6            ┆ 9.106269e6              │
    │ 2024-01-01T0Z ┆ United Nat ┆ Demographics    ┆ 1.8165554e7      ┆ 9.055978e6            ┆ 9.172763e6              │
    └───────────────┴────────────┴─────────────────┴──────────────────┴───────────────────────┴─────────────────────────┘

The demographics model holds lots of submodels and attributes. In this example only a limited number of attributes are listed
as the dataframe is way too large to display. For all models and their details see the model data documentation at
`The DataGarden Data Documentation <https://www.the-datagarden.io/data-docs>`_.

Getting started with the SDK
----------------------------
You can start using the SDK out of the box by simply instatiating the TheDataGardenAPI object:

.. code-block:: python

    # Starting with the datagarden API
    >>> from the-datagarden import TheDataGardenAPI
    >>> the_datagarden_api = TheDataGardenAPI()

.. code-block:: console

    Welcome to The Data Garden API.

      You can start using the API with an account from The-Datagarden.io.
      Please provide your credentials or create a new account.
      Check www.the-datagarden.io for more information.

    Do you want to (1) create a new account or (2) provide existing credentials? Enter 1 or 2:


simply select 1 to create a new account.

.. code-block:: console

    Enrolling in The Data Garden API...

      Enter your email: <your-email>
      Enter your password: <your-password>
      Confirm your password: <your-password>

    Successfully enrolled in The Data Garden API.
    Initializing : TheDatagardenEnvironment
    At: https://www.the-datagarden.io/

If you already have an account at the-datagarden.io, you can either select option 2 or directly provide your credentials
when creating the TheDataGardenAPI object:

.. code-block:: python

    # Retrieve a country object from the datagarden API
    >>> from the-datagarden import TheDataGardenAPI
    >>> the_datagarden_api = TheDataGardenAPI(email='your-email@example.com', password='your-password')

.. code-block:: console

    Initializing : TheDatagardenEnvironment
    At: https://www.the-datagarden.io/

A 3rd way to initialize the SDK is adding your credentials to the ``.env`` file.


Getting your first data from The-DataGarden API
-----------------------------------------------
Now that you have initialized the SDK, you can start retrieving data from The-DataGarden API.
For example, you can retrieve the demographics data for the Netherlands:

.. code-block:: python

    # initialize a country object and retrieve the demographics attribute
    >>> nl = the_datagarden_api.netherlands
    >>> nl_demographics = nl.demographics
    TheDataGardenRegionalDataModel : Demographics : (count=0)

This creates a country object ``nl`` for the Netherlands, which serves as your gateway to all Netherlands-related
data and its regional subdivisions.

In this getting started section we will work with a demographics object retrieved from the `nl` country object.
As shown in the example, the ``nl_demographics`` object can be retrieved by simply calling the `demographics`
attribute on the `nl` country object

The `nl_demographics` object starts empty (count=0). To populate it with data, simply call it as a function:

.. code-block:: python

    # Calling the demographics attribute will populate it with demographics data from the API
    >>> nl_demographics()
    >>> nl_demographics
        TheDataGardenRegionalDataModel : Demographics : (count=5)

When called without parameters, the API returns data using default settings, which in this case yields 5 records.
You can customize your data retrieval by specifying parameters such as time periods, period types, and data sources.


The DataGarden Regional DataModel
---------------------------------
When you retrieve data like ``nl_demographics``, you're working with a ``TheDataGardenRegionalDataModel`` object. This object acts as a container that holds:

1. A collection of ``TheDataGardenRegionalDataRecord`` objects
2. Metadata about the records (region, time period, data source, etc.)

You can easily transform this data into pandas or polars DataFrames for analysis. Here's an example showing population data for the Netherlands:

.. code-block:: python

    >>> nl = the_datagarden_api.netherlands
    >>> nl_demographics = nl.demographics(period_from="2010-01-01", source="united nations")
    >>> # Convert to DataFrame, mapping 'population.total' to column name 'pop_count'
    >>> df = nl_demographics.to_polars({"pop_count": "population.total"}) # or to_pandas(...)
    >>> df["name", "source_name", "period", "data_model_name", "total"] # for readability only a limited number of columns are displayed
        ┌─────────────┬────────────────┬─────────────────┬─────────────────┬─────────────┐
        │ name        ┆ source_name    ┆ period          ┆ data_model_name ┆ pop_count   │
        │ ---         ┆ ---            ┆ ---             ┆ ---             ┆ ---         │
        │ str         ┆ str            ┆ str             ┆ str             ┆ f64         │
        ╞═════════════╪════════════════╪═════════════════╪═════════════════╪═════════════╡
        │ Netherlands ┆ United Nations ┆ 2010-01-010:00Z ┆ Demographics    ┆ 1.6729801e7 │
        │ Netherlands ┆ United Nations ┆ 2011-01-010:00Z ┆ Demographics    ┆ 1.6812669e7 │
        │ …           ┆ …              ┆ …               ┆ …               ┆ …           │
        │ Netherlands ┆ United Nations ┆ 2023-01-010:00Z ┆ Demographics    ┆ 1.8019495e7 │
        │ Netherlands ┆ United Nations ┆ 2024-01-010:00Z ┆ Demographics    ┆ 1.8165554e7 │
        └─────────────┴────────────────┴─────────────────┴─────────────────┴─────────────┘

Each time you call the ``nl_demographics`` object with different parameters,
new demographic records for the specified subregions, periods, and/or sources are added to the existing ``nl_demographics`` object.
After you've gathered all the records you need, you can convert the entire collection into a dataframe for further analysis.


Retrieving GeoJSON data
-----------------------
Retrieving the GeoJSON for the Netherlands and its provinces is straightforward as well:

.. code-block:: python

    >>> nl_geojson = nl.geojsons()
    >>> nl_geojson
        TheDataGardenRegionGeoJSONModel : GeoJSON : (count=1)
    >>> nl_geojson(region_level=2) # Retrieve GeoJSON for 2nd regional level (provinces)
        TheDataGardenRegionGeoJSONModel : GeoJSON : (count=13)  # 12 provinces + 1 country
    >>> df = nl_geojson.to_polars()
    >>> df["name", "region_type", "local_region_code", "region_level", "feature"]
        ┌───────────────┬─────────────┬───────────────┬──────────────┬────────────────────────┐
        │ name          ┆ region_type ┆ local_region_c┆ region_level ┆ feature                │
        │ ---           ┆ ---         ┆ ---           ┆ ---          ┆ ---                    │
        │ str           ┆ str         ┆ str           ┆ i64          ┆ struct[3]              │
        ╞═══════════════╪═════════════╪═══════════════╪══════════════╪════════════════════════╡
        │ Netherlands   ┆ country     ┆ 528           ┆ 0            ┆ {"Feature",{"Netherland│
        │ Drenthe       ┆ province    ┆ NL13          ┆ 2            ┆ {"Feature",{"Drenthe",2│
        │ …             ┆ …           ┆ …             ┆ …            ┆ …                      │
        │ Zuid-Holland  ┆ province    ┆ NL33          ┆ 2            ┆ {"Feature",{"Zuid-Holla│
        └───────────────┴─────────────┴───────────────┴──────────────┴────────────────────────┘

For readability, the output only a limited number of dataframe columns are displayed.
Attributes in both the demographics and geojson dataframes are available to connect the geojson to
the demographics data. This allows you quickly make data sets that contain both demographics and geojson data
for further analysis or visualisation in map applications.


Read more
---------

* `The DataGarden Website <https://www.the-datagarden.io>`_
* `API Documentation <https://www.the-datagarden.io/api-docs>`_
* `The Datagarden Models <https://www.the-datagarden.io/data-docs>`_
* `GitHub Repository <https://github.com/MaartendeRuyter/dg-the-datagarden>`_


Access to The DataGarden API
----------------------------
To use the DataGarden SDK, you need access to the The DataGarden API. Simply register for free at https://www.the-datagarden.io
and you will have an inital free access account to the API with access to country and continent data.

Visit https://www.the-datagarden.io to register for free.
