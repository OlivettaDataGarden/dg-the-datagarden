=============================================
Retrieving more data from The Data Garden API
=============================================

Once you have initiated a RegionalDataModel you can start
requesting more records from the datagarden api.

.. _querying-the-api:

Getting Regional Data
---------------------
Getting more regional data is done by calling RegionalDataModel with the appropriate parameters.

.. code-block:: python

    # Retrieving demographics data for the Netherlands
    >>> nl = api.netherlands # or api.NL
    >>> nl_demographics = nl.demographics
    >>> nl_demographics(period_type="Y", period_from="2010-01-01", period_to="2020-01-01")
    TheDataGardenRegionalDataModel : Demographics : (count=22)

See below the description of parameters that can be used to select the data you want to retrieve.
Although they are described seperately they can be combined to retrieve the data you want.

Selecting the region level
--------------------------
With ``region_level`` you can select for which region level you want to retrieve the data. The ``region_level``
is an int attribute with default value 0 for country data (or continent data) when working with a continent object.

.. code-block:: python

    # Retrieving demographic data for the Netherlands at region level 3
    >>> nl = api.netherlands # or api.NL
    >>> nl_demographics = nl.demographics
    >>> nl_demographics(region_level=3)
    TheDataGardenRegionalDataModel : Demographics : (count=40)


Selecting the period
--------------------
With paramters ``period_from`` and ``period_to`` you can select the period of the data you want to retrieve.
Both dates are inclusive, ie ``period_from="2010-01-01"``, ``period_to="2020-01-01"`` includes records for 2010 up
until and including 2020.
The period parameter should be a string in the format YYYY-MM-DD. Default period range is from 2 years ago to today.

.. code-block:: python

    # Retrieving demographic data for the Netherlands from 2010 to 2020
    >>> nl = api.netherlands # or api.NL
    >>> nl_demographics = nl.demographics
    >>> nl_demographics(period_from="2010-01-01", period_to="2020-01-01")


Selecting the period type
--------------------------
With paramters ``period_type`` you can select the period type of the data you want to retrieve. Possible values are:

- "Y" for yearly (default value)
- "Q" for quarterly
- "M" for monthly
- "W" for weekly
- "D" for daily

Not all datamodels will have data for all period types. This can be checked in the metadata of the datamodel.

.. code-block:: python

    # Retrieving quarterly economics data for the Netherlands
    >>> nl = api.netherlands # or api.NL
    >>> nl_economics = nl.economics
    >>> nl_economics(period_type="Q")
    TheDataGardenRegionalDataModel : Economics : (count=11)


Selecting the data Source
--------------------------
With paramters ``source`` you can select from which original source you want to retrieve the data. The metadata object will
give you which sources are available for a specific datamodel and region. By default data for all sources is returned.
The argument ``source`` should be a string or a list of strings.

.. code-block:: python

    # Retrieving demographic data for the Netherlands from the United Nations
    >>> nl = api.netherlands # or api.NL
    >>> nl_demographics = nl.demographics
    >>> nl_demographics(source=["United Nations"])
    TheDataGardenRegionalDataModel : Demographics : (count=3)

Error feedback
--------------
When a request is made for which no data is available the SDK will return the error message from the API.

.. code-block:: python

    # Retrieving demographic data for a region level that does not have demographic data
    >>> nl = api.netherlands # or api.NL
    >>> nl_demographics = nl.demographics
    >>> nl_demographics(region_level=4)
    value_error
    Provided Data model name in payload unknown or not available for the requested region level/type.
    TheDataGardenRegionalDataModel : demographics : (count=0)

Caching and uniqueness of records
---------------------------------
As long as the ``nl_demographics`` object is in memory the data will remain accessible via the object.
New queries will add new records to the object but records that were already retrieved will not be added to the
nl_demographics object again, keeping each record unique.
The SDK will recognize calls done and will not make a new request for the same call.

.. code-block:: python

    >>> nl = api.netherlands # or api.NL
    >>> nl_demographics = nl.demographics
    >>> nl_demographics()
    TheDataGardenRegionalDataModel : Demographics : (count=6)
    >>> nl_demographics() # will not make a new request
    TheDataGardenRegionalDataModel : Demographics : (count=6)
    >>> nl_demographics(period_from="2010-01-01", period_to="2020-01-01") # will make a new request adding new records
    TheDataGardenRegionalDataModel : Demographics : (count=28)
    >>> nl_demographics(period_from="2015-01-01", period_to="2018-01-01") # will make a new request but no new records
    TheDataGardenRegionalDataModel : Demographics : (count=28)
