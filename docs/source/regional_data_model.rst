===================================
The Regional Data Model, The Basics
===================================

The Basics of the Regional Data Model
-------------------------------------
The regional data model is a class that is used to store regional data records for a given data model.
It is the key object you will use to retrieve and get access to the data from The-Datagarden API.
The object will allow to query the data garden object for specific sources, periods and period types.
Next to the the object provides you with methods to convert the data to pandas or polars dataframes.
Lets look at an example of how to use the object.

.. code-block:: python

    # Retieve a the demographics data model for Germany
    >>> germany = my_datagarden_api.germany
    >>> german_demographics = germany.demographics
    >>> print(german_demographics)

.. code-block:: console

    TheDataGardenRegionalDataModel : demographics : (count=0)

The object is an instance of the TheDataGardenRegionalDataModel thay shows what model it represents and how many records are available.
Upon initialization the object will not have any records. Adding records to the object is done by calling the object.


.. code-block:: python

    # Calling the germany_demographics object will add records to the object
    >>> german_demographics()
    >>> print(german_demographics)

.. code-block:: console

    TheDataGardenRegionalDataModel : demographics : (count=5)

The object now contains 5 records.


Inspecting the structure of the Regional Data Model
---------------------------------------------------
In order to understand what the Regional Data Model contains you can inspect the object.
This is easily done by calling the show_summary() method on the object.

.. code-block:: python

    # Calling the germany_demographics object will add records to the object
    >>> german_demographics()
    >>> german_demographics.show_summary()

.. code-block:: console

    ###### Submodels ######
    Submodel: metadata
         Metadata about the data object instance.
          With attributes:
            - data_is_projection

    Submodel: population
         Population indicators for the region.
          With attributes:
            - by_age_gender
            - total
            - total_male
            - total_female
    ... etc.

    ###### Value attributes ######
    local_regional_data    : Additional source specific data ......

The method provides a comprehensive overview of the model's structure by displaying:

1. All available submodels at top-level model including their submodel attributes
2. The top-level model attributes that directly represent a value

Note that while this summary shows the main structure, it doesn't display the full depth of nested
submodels or the complete details of individual attributes. Some attributes may contain additional
nested structures or complex data types that aren't visible in this overview.

An equivalent method 'summary' exists that returns this info as a dict.

Inspecting the content of the available records
-----------------------------------------------
As soon as there a records in the RegionalDataRecord you can inspect the records by calling the describe() method.

.. code-block:: python

    # initialize the TheDataGardenAPI instance
    >>> german_demographics()
    >>> print(german_demographics.describe())

.. code-block:: console

    ┌────────────┬─────────┬─────────────┬────────────────┬───┬────────────────┬──────────────────────┬─────────────┬─────────────────┐
    │ statistic  ┆ name    ┆ region_type ┆ un_region_code ┆ … ┆ source_name    ┆ period               ┆ period_type ┆ data_model_name │
    │ ---        ┆ ---     ┆ ---         ┆ ---            ┆   ┆ ---            ┆ ---                  ┆ ---         ┆ ---             │
    │ str        ┆ str     ┆ str         ┆ str            ┆   ┆ str            ┆ str                  ┆ str         ┆ str             │
    ╞════════════╪═════════╪═════════════╪════════════════╪═══╪════════════════╪══════════════════════╪═════════════╪═════════════════╡
    │ count      ┆ 5       ┆ 5           ┆ 5              ┆ … ┆ 5              ┆ 5                    ┆ 5           ┆ 5               │
    │ null_count ┆ 0       ┆ 0           ┆ 0              ┆ … ┆ 0              ┆ 0                    ┆ 0           ┆ 0               │
    │ mean       ┆ null    ┆ null        ┆ null           ┆ … ┆ null           ┆ null                 ┆ null        ┆ null            │
    │ std        ┆ null    ┆ null        ┆ null           ┆ … ┆ null           ┆ null                 ┆ null        ┆ null            │
    │ min        ┆ Germany ┆ country     ┆ 276            ┆ … ┆ Eurostat       ┆ 2022-01-01T00:00:00Z ┆ Y           ┆ Demographics    │
    │ 25%        ┆ null    ┆ null        ┆ null           ┆ … ┆ null           ┆ null                 ┆ null        ┆ null            │
    │ 50%        ┆ null    ┆ null        ┆ null           ┆ … ┆ null           ┆ null                 ┆ null        ┆ null            │
    │ 75%        ┆ null    ┆ null        ┆ null           ┆ … ┆ null           ┆ null                 ┆ null        ┆ null            │
    │ max        ┆ Germany ┆ country     ┆ 276            ┆ … ┆ United Nations ┆ 2024-01-01T00:00:00Z ┆ Y           ┆ Demographics    │
    └────────────┴─────────┴─────────────┴────────────────┴───┴────────────────┴──────────────────────┴─────────────┴─────────────────┘
