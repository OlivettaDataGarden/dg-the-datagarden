========================
The Regional Data Record
========================

The RegionalDataRecord class serves as a container for region-specific data entries in the data model system.
Built on `pydantic.BaseModel`, it combines both the actual data and essential contextual information, including:

- Geographic identifiers
- Temporal specifications
- Regional hierarchy details
- Source information

This structured approach ensures that each data point is properly contextualized with its regional and temporal metadata.

Field Descriptions
------------------
.. list-table::
   :header-rows: 1
   :widths: 20 80
   :class: responsive

   * - Field Name
     - Description
   * - name
     - The name of the region
   * - region_type
     - The type of region (e.g., country, state, province, city)
   * - un_region_code
     - United Nations region code identifier
   * - iso_cc_2
     - ISO 3166-1 alpha-2 country code (two-letter country code)
   * - local_region_code
     - Local identifier code for the region
   * - local_region_code_type
     - The type/standard of the local region code
   * - parent_region_code
     - Identifier code of the parent region
   * - parent_region_code_type
     - The type/standard of the parent region code
   * - parent_region_type
     - The type of the parent region (e.g., country for a state)
   * - region_level
     - Integer indicating the hierarchical level of the region (0 being the highest level)
   * - source_name
     - Name of the data source
   * - period
     - Time period for the data
   * - period_type
     - Type of time period (e.g., year, month, quarter)
   * - data_model_name
     - The data model name
   * - model
     - The actual data provide as a `The DataGardenModel` instance


If you wish you access the data objects from the RegionalRecordModel instance

.. code-block:: python

    # retrieve the data object from the RegionalRecordModel instance
    >>> from from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()
    >>> germany_demographics = my_datagarden_api.germany.demographics
    >>> germany_demographics(from_date="2015-01-01")
    >>> record_list: list[RegionalDataRecord] = germany_demographics.data_records
    >>> print(record_list[0])
    >>> print(type(record_list[0]))

Inspecting the first record in the list will give you the following output:

.. code-block:: console

    RegionalDataRecord: Germany (Demographics for 2015-01-01T00:00:00Z, Y)
    <class 'the_datagarden.models.RegionalDataRecord'>

In general it should not be necessary to access the RegionalDataRecord instances directly, but it can be useful
to do so for debugging and inspection purposes.
