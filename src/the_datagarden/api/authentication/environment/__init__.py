from the_datagarden.abc import DatagardenEnvironment

from ..credentials import TheDataGardenCredentials


class TheDatagardenProductionEnvironment(DatagardenEnvironment):
    CREDENTIALS = TheDataGardenCredentials
    THE_DATAGARDEN_URL = "https://api.the-datagarden.io"


class TheDatagardenLocalEnvironment(DatagardenEnvironment):
    CREDENTIALS = TheDataGardenCredentials
    THE_DATAGARDEN_URL = "http://127.0.0.1:8000"
