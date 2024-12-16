====================================
Working with The Regional Data Model
====================================


Structure of the Regional Data Model
------------------------------------
The Regional Data Model stores data for a specific model (such as demographics) for a region and its subregions.
Each record combines the actual DataGarden DataModel data with metadata including:

* Region reference
* Time period
* Period type (e.g., yearly, monthly)
* Data source

This structure allows you to filter and query the data across all these dimensions.

See :doc:`regional_data_record` for more details about the available record attributes.


Converting to pandas or polars dataframes
-----------------------------------------
The first step to working with the Regional Data Model is to convert it to a pandas or polars dataframe.

.. code-block:: python

    # Retieve a the demographics data model for Germany
    >>> germany = my_datagarden_api.germany
    >>> german_demographics = germany.demographics
    >>> df = german_demographics.full_model_to_polars() # or full_model_to_pandas()


This will return a polars dataframe with all the data from the DataGarden DataModel. All field names are flattend based upon nested model and attribute names.
For example the total attribute from the population submodel will be flattened to population.total. Denpending on tge model this can become a very wide dataframe.
If you are only interested in a specific attribute you can use the to_polars() or to_pandas() method with a dictionary of model attributes to convert to columns.


.. code-block:: python

    # Retieve a the demographics data model for Germany
    >>> germany = my_datagarden_api.germany
    >>> german_demographics = germany.demographics
    >>> df = german_demographics.to_polars({"pop_count": "population.total"}) # or to_pandas(...)

Now the dataframe contains only the pop_count column incombination with all metdata data columnns



Working with submodels
----------------------
If you wish to work only with a submodel you can use the submodel name as an attribute., This will return a new RegionalDataModel object with only the submodel data.
This is useful if you as you can now directly access the attributes of the submodel instead of having to use the dot notation.


.. code-block:: python

    # Retieve a the demographics data model for Germany
    >>> germany = my_datagarden_api.germany
    >>> german_demographics = germany.demographics
    >>> german_population = german_demographics.population
    >>> df = german_population.to_polars({"pop_count": "total"})
    # or
    >>> df_all = german_population.full_model_to_polars() # now returns a dataframe with only the attributes of the population submodel

If needed you can go deeper and call submodels of the submodel.

These DatagardenModel objects can not be used to retrieve additional records from the TheDataGardenAPI. This can only be done on the main model.
