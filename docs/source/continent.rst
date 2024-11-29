================
Continent Object
================
The continent object provides methods to get data on a continent or to access subregion (countries) objects from the continent.

To get an overview of which data models are available for a continent object, you can call
the `available_model_names`  method on the TheDataGardenAPI continent object:

.. code-block:: python

    # Retrieving available data models for Europe
    >>> from from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> europe = my_datagarden_api.europe
    >>> print(europe.available_model_names)

.. code-block:: console

    ['Economics', 'Demographics']

This method returns a list of available data models.

If you want to get more information about the available datamodels, you can call the `available_models` method:

.. code-block:: python

    # Retrieving detailed information about the available data models
    >>> europe = my_datagarden_api.europe
    >>> print(europe.available_models)


This returns a dictionary with the continent names as keys and the continent objects as values:

.. code-block:: json

    {
        "Economics": {
            "count": 19,
            "sources": ["UNCTAD"],
            "to_period": "2023-01-01T00:00:00Z",
            "from_period": "2005-01-01T00:00:00Z",
            "period_type": ["Y"],
        },
        "Demographics": {
            "count": 151,
            "sources": ["United Nations"],
            "to_period": "2100-01-01T00:00:00Z",
            "from_period": "1950-01-01T00:00:00Z",
            "period_type": ["Y"],
        },
    }



Now that we can see what data models are available, you can retrieve the data by calling the data model name on the continent object:

.. code-block:: python

    # Retrieving demographic data for Europe
    >>> europe = my_datagarden_api.europe
    >>> europe_demographics = europe.demographics
    >>> print(europe_demographics)


This data model method returns an object of type TheDataGardenRegionalDataModel:

.. code-block:: console

    TheDataGardenRegionalDataModel : Demographics : (count=5)

How you can use this class to extract and use the data is described in the :doc:`regional_data_model` page.
Here it is sufficient to know that an instance of this class holds a list of RegionalDataRecord instances.
Each RegionalDataRecord instance contains the data for a unique combination of region, source, period and period type.
You can quickly view the available data by converting the object to a Polars or Pandas dataframe:

.. code-block:: python

    >>> europe = my_datagarden_api.europe
    >>> europe_df = europe.to_polars()  # or europe.to_pandas()
    >>> print(europe_df.head())
    >>> print(europe_df.columns)

.. code-block:: console

    ┌────────┬─────────────┬────────────────┬──────────┬───┬────────────────┬──────────────────────┬─────────────┬──────────────┐
    │ name   ┆ region_type ┆ un_region_code ┆ iso_cc_2 ┆ … ┆ source_name    ┆ period               ┆ period_type ┆ data_type    │
    │ ---    ┆ ---         ┆ ---            ┆ ---      ┆   ┆ ---            ┆ ---                  ┆ ---         ┆ ---          │
    │ str    ┆ str         ┆ str            ┆ str      ┆   ┆ str            ┆ str                  ┆ str         ┆ str          │
    ╞════════╪═════════════╪════════════════╪══════════╪═══╪════════════════╪══════════════════════╪═════════════╪══════════════╡
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2020-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2021-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2022-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2023-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    │ Europe ┆ continent   ┆ 908            ┆ __       ┆ … ┆ United Nations ┆ 2024-01-01T00:00:00Z ┆ Y           ┆ Demographics │
    └────────┴─────────────┴────────────────┴──────────┴───┴────────────────┴──────────────────────┴─────────────┴──────────────┘
    ['name', 'region_type', 'un_region_code', 'iso_cc_2', 'local_region_code', 'local_region_code_type', 'parent_region_code',
    'parent_region_code_type', 'parent_region_type', 'region_level', 'source_name', 'period', 'period_type', 'data_type']


Notice that europe_df.columns does not contain any columns for the actual demographics data.
This is because the to_polars() method only adds specified data columns by default.
To see the complete data in the dataframe, use the full_models_to_polars() method instead.
This will add a fully flattened version of the Demographics data model to the dataframe.
For more options to control what data is added to the dataframe, see the :doc:`regional_data_model` page.

Both methods are also available as pandas methods (`to_pandas()` and `full_models_to_pandas()`).
