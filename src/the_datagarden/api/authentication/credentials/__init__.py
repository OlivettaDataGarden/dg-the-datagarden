import requests
from decouple import config

from the_datagarden.abc.authentication import BaseDataGardenCredentials, TheDatagardenCredentialsDict
from the_datagarden.api.authentication.settings import REGISTRATION_URL_EXTENSION


class CredentialsFromUserInput:
    def get_missing_credentials(self, the_datagarden_api_url: str) -> TheDatagardenCredentialsDict:
        print()
        print("Welcome to The Data Garden API.")
        print()
        print("  You can start using the API with an account from The-Datagarden.io.")
        print("  Please provide your credentials or create a new account.")
        print("  Check www.the-datagarden.io for more information.")
        print()
        choice = input(
            "Do you want to (1) create a new account or (2) provide existing credentials? " "Enter 1 or 2: "
        )

        if choice == "1":
            credentials = self.enroll_to_api(the_datagarden_api_url)
            if not credentials:
                quit()
            return credentials

        elif choice == "2":
            return self.provide_existing_credentials()
        else:
            print("Invalid choice. Please enter 1 or 2.")
            return self.get_missing_credentials(the_datagarden_api_url)

    def enroll_to_api(self, the_datagarden_api_url: str) -> TheDatagardenCredentialsDict | None:
        print("Enrolling in The Data Garden API...")
        print()
        email = input("  Enter your email: ")
        password = self.get_confirmed_password()
        print()

        data = {"email": email, "password": password}
        registration_url = the_datagarden_api_url + REGISTRATION_URL_EXTENSION
        response = requests.post(registration_url, data=data)
        if response.status_code == 201:
            print("Successfully enrolled in The Data Garden API.")
            return TheDatagardenCredentialsDict(
                email=email,
                password=password,
            )
        else:
            print("Enrollment failed with error(s):")
            for field, message_list in response.json().items():
                print(f"    {field}: {message_list[0]}")

        return None

    def get_confirmed_password(self) -> str:
        while True:
            password = input("  Enter your password: ")
            confirm_password = input("  Confirm your password: ")

            if password == confirm_password:
                return password
            else:
                print("Passwords do not match. Please try again.")

    def provide_existing_credentials(self) -> TheDatagardenCredentialsDict:
        print("Please provide your existing credentials...")
        print()
        email = input("  Enter your email: ")
        password = input("  Enter your password: ")
        return TheDatagardenCredentialsDict(
            email=email,
            password=password,
        )

    def credentials(self, the_datagarden_api_url: str) -> TheDatagardenCredentialsDict:
        return self.get_missing_credentials(the_datagarden_api_url)


class TheDataGardenCredentials(BaseDataGardenCredentials):
    """
    Manages credentials for The Data Garden API in a production environment.

    This class handles the retrieval of user credentials (email and password) for
    authenticating with The Data Garden API. It first attempts to fetch credentials
    from environment variables. If not found, it prompts the user for input.

    Attributes:
        ENV_EMAIL_KEY (str): Environment variable key for the user's email.
        ENV_PASSWORD_KEY (str): Environment variable key for the user's password.
        CREDENTIALS_FROM_USER_INPUT (CredentialsFromUserInput):
                Instance to handle user input for credentials.

    Methods:
        credentials(): Retrieves and returns the user's credentials.
    """

    ENV_EMAIL_KEY: str = "THE_DATAGARDEN_USER_EMAIL"
    ENV_PASSWORD_KEY: str = "THE_DATAGARDEN_USER_PASSWORD"
    CREDENTIALS_FROM_USER_INPUT = CredentialsFromUserInput()

    @classmethod
    def credentials(
        cls, the_datagarden_api_url: str, email: str | None = None, password: str | None = None
    ) -> TheDatagardenCredentialsDict:
        if email and password:
            return TheDatagardenCredentialsDict(
                email=email,
                password=password,
            )

        datagarden_user_email = str(config(cls.ENV_EMAIL_KEY, default="", cast=str))
        datagarden_user_password = str(config(cls.ENV_PASSWORD_KEY, default="", cast=str))
        if datagarden_user_email and datagarden_user_password:
            return TheDatagardenCredentialsDict(
                email=datagarden_user_email,
                password=datagarden_user_password,
            )

        return cls.CREDENTIALS_FROM_USER_INPUT.credentials(the_datagarden_api_url)
