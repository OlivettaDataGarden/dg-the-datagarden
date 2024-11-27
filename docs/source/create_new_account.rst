=============
A new account
=============
In order to use the The-DataGarden API, you to have an account. If you do not have one yet
you can directly enroll from the Python SDK. This will create a free account for you with limited access.
For getting more access to the different models see `The-DataGarden website <https://www.the-datagarden.io>`_.

If you use the TheDataGardenAPI object without providing any credentials, you can choose to direcly create an account in the API.


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
