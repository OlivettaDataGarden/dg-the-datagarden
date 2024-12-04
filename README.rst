==================
the-datagarden SDK
==================

The-datagarden package is a Python SDK built on top of The-DataGarden API. It provides easy access to continent and country regional hierarchies, as well as public data related to these regions. Additionally, you can retrieve regional GeoJSONs using the SDK. It simplifies the process of converting regional data into DataFrames and/or GeoJSON Feature collections, enabling developers to build upon this data effortlessly.

A quick example
---------------
If you have a user account at the-datagarden.io, you can start using the SDK right away:

.. code-block:: python

    # Retrieve a country object from the datagarden API
    >>> from the-datagarden import TheDataGardenAPI
    >>> the_datagarden_api = TheDataGardenAPI(email='your-email@example.com', password='your-password')
    >>> nl = the_datagarden_api.netherlands()
    >>> nl_demographics = nl.demographics(from_period="2010-01-01", source="united nations")
    >>> nl_demographics
        TheDataGardenRegionalDataModel : Demographics : (count=15)

this returns a `TheDataGardenRegionalDataModel` containimg the demographics data in this case 15 records.
Each of those records will contain a Demographics object for the region for the specified period.

To work with this data, you can convert it to a pandas or polars dataframe and select the data from the demographics
data model you need.

.. code-block:: python

    >>> df = nl_demographics.to_polars({"pop_count": "population.total"}) # or to_pandas(...)
    >>> df["name", "source_name", "period", "data_model_name", "total"]
        ┌─────────────┬────────────────┬─────────────────┬─────────────────┬─────────────┐
        │ name        ┆ source_name    ┆ period          ┆ data_model_name ┆ pop_count   │
        │ ---         ┆ ---            ┆ ---             ┆ ---             ┆ ---         │
        │ str         ┆ str            ┆ str             ┆ str             ┆ f64         │
        ╞═════════════╪════════════════╪═════════════════╪═════════════════╪═════════════╡
        │ Netherlands ┆ United Nations ┆ 2010-01-010:00Z ┆ Demographics    ┆ 1.6729801e7 │
        │ Netherlands ┆ United Nations ┆ 2011-01-010:00Z ┆ Demographics    ┆ 1.6812669e7 │
        │ Netherlands ┆ United Nations ┆ 2012-01-010:00Z ┆ Demographics    ┆ 1.6889445e7 │
        │ Netherlands ┆ United Nations ┆ 2013-01-010:00Z ┆ Demographics    ┆ 1.6940942e7 │
        │ Netherlands ┆ United Nations ┆ 2014-01-010:00Z ┆ Demographics    ┆ 1.6993184e7 │
        │ …           ┆ …              ┆ …               ┆ …               ┆ …           │
        │ Netherlands ┆ United Nations ┆ 2020-01-010:00Z ┆ Demographics    ┆ 1.7601682e7 │
        │ Netherlands ┆ United Nations ┆ 2021-01-010:00Z ┆ Demographics    ┆ 1.767178e7  │
        │ Netherlands ┆ United Nations ┆ 2022-01-010:00Z ┆ Demographics    ┆ 1.7789347e7 │
        │ Netherlands ┆ United Nations ┆ 2023-01-010:00Z ┆ Demographics    ┆ 1.8019495e7 │
        │ Netherlands ┆ United Nations ┆ 2024-01-010:00Z ┆ Demographics    ┆ null        │
        └─────────────┴────────────────┴─────────────────┴─────────────────┴─────────────┘


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
        │ Flevoland     ┆ province    ┆ NL23          ┆ 2            ┆ {"Feature",{"Flevoland"│
        │ Friesland     ┆ province    ┆ NL12          ┆ 2            ┆ {"Feature",{"Friesland"│
        │ Gelderland    ┆ province    ┆ NL22          ┆ 2            ┆ {"Feature",{"Gelderland│
        │ …             ┆ …           ┆ …             ┆ …            ┆ …                      │
        │ Noord-Holland ┆ province    ┆ NL32          ┆ 2            ┆ {"Feature",{"Noord-Holl│
        │ Overijssel    ┆ province    ┆ NL21          ┆ 2            ┆ {"Feature",{"Overijssel│
        │ Utrecht       ┆ province    ┆ NL31          ┆ 2            ┆ {"Feature",{"Utrecht",2│
        │ Zeeland       ┆ province    ┆ NL34          ┆ 2            ┆ {"Feature",{"Zeeland",2│
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

Visit https://www.the-datagarden.io for to register for free.
