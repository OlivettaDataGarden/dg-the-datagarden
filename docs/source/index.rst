.. the-datagarden documentation master file, created by
   sphinx-quickstart on Mon Nov 25 20:22:02 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

the-datagarden documentation
============================

The-datagarden package is SDK on top of the The-DataGarden API. The SDK makes it easy for you to retrieve
public data from The-DataGarden API, and locally enrich the public data with your own data. On top of that,
the SDK provides additional methods to do statistical analysis and calculations with the public data retrieved.




Getting started
---------------
If you already have a user account at the-datagarden.io you can directly start using the SDK ::

    # retrieve country object from the datagarden api
    >>> from the-datagarden import TheDataGardenAPI
    >>> the_datagarden_api = TheDataGardenAPI(email='your-email@example.com', password='your-password')
    >>> nl = the_datagarden_api.netherlands()
    >>> print(nl)

    Country(
        name='Netherlands',
        iso_code='NL')


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   authentication
   create_new_account
   the_datagarden_api
   continent
