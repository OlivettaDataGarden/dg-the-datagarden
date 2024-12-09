==============
Authentication
==============
In order to use the The-DataGarden API, you need to authenticate yourself. This can be done by providing your
credentials to the TheDataGardenAPI object.

Authenticating
--------------

When you already have an account, you can authenticate by providing your email and password to the TheDataGardenAPI object.
There are three ways to do that:

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



Creating an account
-------------------

If you do not have an account yet, you can directly enroll from the Python SDK. This will create a free account for you with access to the country and continent data.
For getting more access to the different region types and models see `The-DataGarden website <https://www.the-datagarden.io>`_.

Creating an account via the SDK can simply be done by calling the TheDataGardenAPI object without providing any credentials:


.. code-block:: python

    # Authenticate by entering email and password via screen
    >>> from from the_datagarden import TheDataGardenAPI
    >>> my_datagarden_api = TheDataGardenAPI()

.. code-block:: console

    Initializing : TheDatagardenProductionEnvironment

    Credentials to access The Data Garden API are missing.
    Do you want to (1) enroll in the API or (2) provide existing credentials? Enter 1 or 2: 1
    Enrolling in The Data Garden API...
    Enter your email: <your-email>
    Enter your password: <your-password>
    Confirm your password: <your-password>
    Successfully enrolled in The Data Garden API.
    Initializing : TheDatagardenProductionEnvironment

A account is now created and you can start using the API. You will be send and email with confirmation of your account.
