==============
Authentication
==============
In order to use the The-DataGarden API, you need to authenticate yourself. This can be done by providing your
credentials to the TheDataGardenAPI object. There three ways to do that:

.. code-block:: python

    # Authenticate by providing email and password to the TheDataGardenAPI istance
    >>> from from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI(email=<your-email>, password=<your-password>)

.. code-block:: console

    Initializing : TheDatagardenProductionEnvironment

or:

.. code-block:: python

    # Authenticate by entering email and password via screen
    >>> from from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()

.. code-block:: console

    Credentials to access The Data Garden API are missing.
    Do you want to (1) enroll in the API or (2) provide existing credentials? Enter 1 or 2: 2
    Please provide your existing credentials...
    Enter your email: <your-email>
    Enter your password: <your-password>
    Initializing : TheDatagardenProductionEnvironment

or setting the environment variables ``THE_DATAGARDEN_USER_EMAIL`` and ``THE_DATAGARDEN_USER_PASSWORD`` in .env:

.. code-block:: bash

    # set the environment variables
    $ echo "THE_DATAGARDEN_USER_EMAIL=<your-email>" >> .env
    $ echo "THE_DATAGARDEN_USER_PASSWORD=<your-password>" >> .env

Once these variables are set, you can initialize the TheDataGardenAPI instance without providing any credentials:

.. code-block:: python

    # initialize the TheDataGardenAPI instance
    >>> from from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()

.. code-block:: console

    Initializing : TheDatagardenProductionEnvironment
