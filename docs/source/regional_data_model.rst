=======================
The Regional Data Model
=======================

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

The object is an instance of the ``TheDataGardenRegionalDataModel`` thay shows what model it represents and how many records are available.
Upon initialization the object will not have any records. Adding records to the object is done by calling the object.


.. code-block:: python

    # Calling the germany_demographics object will add records to the object
    >>> german_demographics()
    >>> print(german_demographics)

.. code-block:: console

    TheDataGardenRegionalDataModel : demographics : (count=5)

The object now contains 5 records.

.. _inspecting-data-model-structure:

Inspecting the structure of the Regional Data Model
---------------------------------------------------
In order to understand what the Regional Data Model contains you can inspect the object or check the websites data documentation `here <https://www.the-datagarden.io/data-docs>`_.
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

.. _inspecting-the-content-of-the-available-records:

Inspecting the content of the available records
-----------------------------------------------
As soon as there a records in the RegionalDataRecord you can inspect the records by calling the describe() method.

.. code-block:: python

    # initialize the TheDataGardenAPI instance
    >>> german_demographics()
    >>> print(german_demographics.describe())

.. code-block:: console

    ┌────────────┬─────────────────────┬───────────────────────────┬───────────────────────────┬───┬───────────────────────────┬──────────────────────────┬──────────────────────────┬──────────────────────────┐
    │ statistic  ┆ local_regional_data ┆ metadata.data_is_projecti ┆ population.by_age_gender. ┆ … ┆ fertility.births_by_age.A ┆ fertility.births_by_age. ┆ fertility.births_by_age. ┆ fertility.births_by_age. │
    │ ---        ┆ ---                 ┆ on                        ┆ male.…                    ┆   ┆ GE-46                     ┆ AGE-47                   ┆ AGE-48                   ┆ AGE-49                   │
    │ str        ┆ f64                 ┆ ---                       ┆ ---                       ┆   ┆ ---                       ┆ ---                      ┆ ---                      ┆ ---                      │
    │            ┆                     ┆ f64                       ┆ f64                       ┆   ┆ f64                       ┆ f64                      ┆ f64                      ┆ f64                      │
    ╞════════════╪═════════════════════╪═══════════════════════════╪═══════════════════════════╪═══╪═══════════════════════════╪══════════════════════════╪══════════════════════════╪══════════════════════════╡
    │ count      ┆ 0.0                 ┆ 5.0                       ┆ 5.0                       ┆ … ┆ 3.0                       ┆ 3.0                      ┆ 3.0                      ┆ 3.0                      │
    │ null_count ┆ 5.0                 ┆ 0.0                       ┆ 0.0                       ┆ … ┆ 2.0                       ┆ 2.0                      ┆ 2.0                      ┆ 2.0                      │
    │ mean       ┆ null                ┆ 0.2                       ┆ 400053.4                  ┆ … ┆ 690.0                     ┆ 339.666667               ┆ 121.0                    ┆ 16.0                     │
    │ std        ┆ null                ┆ null                      ┆ 15455.892769              ┆ … ┆ 64.784257                 ┆ 38.527047                ┆ 10.535654                ┆ 1.0                      │
    │ min        ┆ null                ┆ 0.0                       ┆ 376468.0                  ┆ … ┆ 629.0                     ┆ 302.0                    ┆ 110.0                    ┆ 15.0                     │
    │ 25%        ┆ null                ┆ null                      ┆ 397477.0                  ┆ … ┆ 683.0                     ┆ 338.0                    ┆ 122.0                    ┆ 16.0                     │
    │ 50%        ┆ null                ┆ null                      ┆ 401359.0                  ┆ … ┆ 683.0                     ┆ 338.0                    ┆ 122.0                    ┆ 16.0                     │
    │ 75%        ┆ null                ┆ null                      ┆ 406078.0                  ┆ … ┆ 758.0                     ┆ 379.0                    ┆ 131.0                    ┆ 17.0                     │
    │ max        ┆ null                ┆ 1.0                       ┆ 418885.0                  ┆ … ┆ 758.0                     ┆ 379.0                    ┆ 131.0                    ┆ 17.0                     │
    └────────────┴─────────────────────┴───────────────────────────┴───────────────────────────┴───┴───────────────────────────┴──────────────────────────┴──────────────────────────┴──────────────────────────┘

The dataframe wll be very wide if you run the describe() method omn the top level model.
there are two ways to make the output more readable.

1. Select a submodel and call the describe() method on the submodel.
2. Use the include_attributes parameter to only include the attributes you are interested in.

.. code-block:: python

    # Select a submodel and call the describe() method on the submodel.
    >>> print(german_demographics.population.describe()) # returns the describe for the full population submodel
    >>> print(german_demographics.describe(include_attributes=['population.total'])) # returns the describe for the total attribute of the population submodel

You can also combine the two methods in a single call

.. code-block:: python

    # Select a submodel and call the describe() method on the submodel.
    >>> print(german_demographics.population.describe(include_attributes=['total'])) # no prefix 'population.' needed as the submodel is already selected

If you are only interested in the subscribe result of a limited set of records you can use a filter.

.. code-block:: python

    # initialize the TheDataGardenAPI instance
    >>> import polars as pl
    >>> german_demographics()
    >>> german_demographics.describe(filter_expr=(pl.col('source_name') == 'United Nations'))
    >>> german_demographics.describe(filter_expr=(pl.col('period') > '2024'))

The filter_expr parameter is a polars expression as The-Datagarden sdk works with polars internally.

To get a quick overview of the available data a method is available that outputs all fields in combination
with count and null_count statistics.

.. code-block:: python

    # initialize the TheDataGardenAPI instance
    >>> import polars as pl
    >>> german_demographics(period_from='2000-01-01')
    >>> population = german_demographics.population
    >>> population.data_availability_per_attribute(
            filter_expr=(
                pl.col("source_name") == "United Nations",
                pl.col("period") > "2015"
            ),
            include_attributes=['total']
    )

This returns the default dataframe for the polars describe() method for the ``total``
attribute of the ``population`` submodel.

.. code-block:: console

    ┌────────────┬───────────────┐
    │ statistic  ┆ total         │
    │ ---        ┆ ---           │
    │ str        ┆ f64           │
    ╞════════════╪═══════════════╡
    │ count      ┆ 10.0          │
    │ null_count ┆ 0.0           │
    │ mean       ┆ 8.3397e7      │
    │ std        ┆ 889695.196625 │
    │ min        ┆ 8.1589465e7   │
    │ 25%        ┆ 8.2954569e7   │
    │ 50%        ┆ 8.362261e7    │
    │ 75%        ┆ 8.3771555e7   │
    │ max        ┆ 8.4695563e7   │
    └────────────┴───────────────┘

You can also view the null_count vs the total count (in this example for all fields in the population submodel)

.. code-block:: python

    # initialize the TheDataGardenAPI instance
    >>> import polars as pl
    >>> german_demographics(period_from='2000-01-01')
    >>> population = german_demographics.population
    >>> population.show_data_availability_per_attribute(
            filter_expr=(
                pl.col("source_name") == "United Nations",
                pl.col("period") > "2015"
            ),
    )
    metadata.data_is_projection :                        10 of which with data: 10 (100%)
    population.by_age_gender.male.AGE-1 :                10 of which with data: 10 (100%)
    population.by_age_gender.male.AGE-1 :                10 of which with data: 10 (100%)
    population.by_age_gender.male.AGE-2 :                10 of which with data: 10 (100%)
    population.by_age_gender.male.AGE-3 :                10 of which with data: 10 (100%)
    ......
