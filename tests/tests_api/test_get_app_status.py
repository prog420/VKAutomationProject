import allure
import pytest
from tests_api.base_case import BaseAPICase
from test_data.api_data import APIData


@allure.epic("API")
@allure.feature("/status - Get App Status")
class TestGetAppStatusAPI(BaseAPICase):
    @pytest.mark.API
    @pytest.mark.parametrize(
        "title, test_case_link, method, expected_status",
        [test_case["case"] for test_case in APIData.get_status_data],
        ids=[test_case["case"][0] for test_case in APIData.get_status_data]
    )
    def test_if_user_can_get_app_status(self, title, test_case_link, method, expected_status):
        """
        Test if user can get app status
        :param title: name of the test
        :param test_case_link: link to test documented in Notion
        :param method: HTTP method for request
        :param expected_status: Expected status code
        """
        allure.dynamic.title(title)
        allure.dynamic.link(test_case_link, name='Test Case')
        response = self.api_client.get_status(method=method, expected_status=expected_status)
