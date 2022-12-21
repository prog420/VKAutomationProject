import pytest
from app.api.client.main_api import AppAPIClient


class BaseAPICase:
    base_url = None
    sql_client = None
    api_client = None
    api_client_no_auth = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, sql_client):
        host = "localhost"
        port = "8082"
        self.base_url = f"http://{host}:{port}"
        self.sql_client = sql_client
        self.api_client = AppAPIClient(
            base_url=self.base_url, auth=True, username="RootUser", password="RootPass"
        )
        self.api_client_no_auth = AppAPIClient(
            base_url=f"http://{host}:{port}", auth=False
        )
