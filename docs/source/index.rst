==================
the-datagarden SDK
==================

The-datagarden package is a pyhton SDK on top of the The-DataGarden API. The SDK gives you easy access to continent and country
regional hierarchies, and to the public data associated with these regions. Also the regional Geojsons can be retrieved from the SDK.
The SDK makes it easy to convert (parts of) the regional data to Dataframes and/or Geojson Feature collections so that you as a developer
can easily build on top of that.



A quick example
---------------
If you already have a user account at the-datagarden.io you can directly start using the SDK ::

    # retrieve country object from the datagarden api
    >>> from the-datagarden import TheDataGardenAPI
    >>> the_datagarden_api = TheDataGardenAPI(email='your-email@example.com', password='your-password')
    >>> nl = the_datagarden_api.netherlands()
    >>> nl_demographics = nl.demographics(from_period="2010-01-01", source="united nations")
    >>> print(nl_demographics)
        TheDataGardenRegionalDataModel : Demographics : (count=15)
    >>> df = nl_demographics.to_polars() # or to_panndas()
    >>> print(df["name", "source_name", "period", "data_model_name", "total"])
   ┌─────────────┬────────────────┬──────────────────────┬─────────────────┬─────────────┐
   │ name        ┆ source_name    ┆ period               ┆ data_model_name ┆ total       │
   │ ---         ┆ ---            ┆ ---                  ┆ ---             ┆ ---         │
   │ str         ┆ str            ┆ str                  ┆ str             ┆ f64         │
   ╞═════════════╪════════════════╪══════════════════════╪═════════════════╪═════════════╡
   │ Netherlands ┆ United Nations ┆ 2010-01-01T00:00:00Z ┆ Demographics    ┆ 1.6729801e7 │
   │ Netherlands ┆ United Nations ┆ 2011-01-01T00:00:00Z ┆ Demographics    ┆ 1.6812669e7 │
   │ Netherlands ┆ United Nations ┆ 2012-01-01T00:00:00Z ┆ Demographics    ┆ 1.6889445e7 │
   │ Netherlands ┆ United Nations ┆ 2013-01-01T00:00:00Z ┆ Demographics    ┆ 1.6940942e7 │
   │ Netherlands ┆ United Nations ┆ 2014-01-01T00:00:00Z ┆ Demographics    ┆ 1.6993184e7 │
   │ …           ┆ …              ┆ …                    ┆ …               ┆ …           │
   │ Netherlands ┆ United Nations ┆ 2020-01-01T00:00:00Z ┆ Demographics    ┆ 1.7601682e7 │
   │ Netherlands ┆ United Nations ┆ 2021-01-01T00:00:00Z ┆ Demographics    ┆ 1.767178e7  │
   │ Netherlands ┆ United Nations ┆ 2022-01-01T00:00:00Z ┆ Demographics    ┆ 1.7789347e7 │
   │ Netherlands ┆ United Nations ┆ 2023-01-01T00:00:00Z ┆ Demographics    ┆ 1.8019495e7 │
   │ Netherlands ┆ United Nations ┆ 2024-01-01T00:00:00Z ┆ Demographics    ┆ null        │
   └─────────────┴────────────────┴──────────────────────┴─────────────────┴─────────────┘


Retrieve the GeoJSON for the netherlands and its provinces is easy as well ::

    >>> nl_geojson = nl.geojsons()
    >>> print(nl_geojson)
        TheDataGardenRegionGeoJSONModel : GeoJSON : (count=1)
   # retrieve the geojson for 2nd regional level in the hierarchy which are the provinces
    >>> nl_geojson(region_level=2)
    >>> print(nl_geojson)
        TheDataGardenRegionGeoJSONModel : GeoJSON : (count=13)  # 12 provinces + 1 country
    >>> df = nl_geojson.to_polars()
    >>> print(df["name", "region_type", "local_region_code", "region_level", "feature"])
    ┌───────────────┬─────────────┬───────────────────┬──────────────┬──────────────────────────┐
    │ name          ┆ region_type ┆ local_region_code ┆ region_level ┆ feature                  │
    │ ---           ┆ ---         ┆ ---               ┆ ---          ┆ ---                      │
    │ str           ┆ str         ┆ str               ┆ i64          ┆ struct[3]                │
    ╞═══════════════╪═════════════╪═══════════════════╪══════════════╪══════════════════════════╡
    │ Netherlands   ┆ country     ┆ 528               ┆ 0            ┆ {"Feature",{"Netherlands"│
    │ Drenthe       ┆ province    ┆ NL13              ┆ 2            ┆ {"Feature",{"Drenthe",2,"│
    │ Flevoland     ┆ province    ┆ NL23              ┆ 2            ┆ {"Feature",{"Flevoland",2│
    │ Friesland     ┆ province    ┆ NL12              ┆ 2            ┆ {"Feature",{"Friesland",2│
    │ Gelderland    ┆ province    ┆ NL22              ┆ 2            ┆ {"Feature",{"Gelderland",│
    │ …             ┆ …           ┆ …                 ┆ …            ┆ …                        │
    │ Noord-Holland ┆ province    ┆ NL32              ┆ 2            ┆ {"Feature",{"Noord-Hollan│
    │ Overijssel    ┆ province    ┆ NL21              ┆ 2            ┆ {"Feature",{"Overijssel",│
    │ Utrecht       ┆ province    ┆ NL31              ┆ 2            ┆ {"Feature",{"Utrecht",2,"│
    │ Zeeland       ┆ province    ┆ NL34              ┆ 2            ┆ {"Feature",{"Zeeland",2,"│
    │ Zuid-Holland  ┆ province    ┆ NL33              ┆ 2            ┆ {"Feature",{"Zuid-Holland│
    └───────────────┴─────────────┴───────────────────┴──────────────┴──────────────────────────┘


Note that for readibility the output of the print statements only a limited number of columns is shown.
Both in the demographics dataframe and the geojson dataframe attributes are available to connect the
two dataframes.

In oder to be able to work with the DataGarden SDK you will need to have an account at the-datagarden.

See https://www.the-datagarden.io for details on how to start for free. Also check out the :doc:`authentication`.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   the_datagarden_api
   continent
   country
   authentication
   create_new_account
   regional_data_model
   regional_data_record
