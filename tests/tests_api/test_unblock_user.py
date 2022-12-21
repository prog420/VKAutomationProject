import allure
import pytest
from tests_api.base_case import BaseAPICase
from test_data.api_data import APIData


@allure.epic("API")
@allure.feature("/api/user/<username>/accept - Unblock User")
class TestUnblockUserAPI(BaseAPICase):
    @pytest.mark.API
    @pytest.mark.parametrize(
        "title, test_case_link, user, method, expected_status",
        [test_case["case"] for test_case in APIData.unblock_user_data],
        ids=[test_case["case"][0] for test_case in APIData.unblock_user_data]
    )
    def test_unblock_user(self, title, test_case_link, user, method, expected_status):
        """
        Test if user can be unblocked
        :param title: name of the test
        :param test_case_link: link to test documented in Notion
        :param user: User data for database
        :param method: HTTP method for request
        :param expected_status: Expected status code
        """
        allure.dynamic.title(title)
        allure.dynamic.link(url=test_case_link, name="Test Case")
        # Add User to database if needed
        if user.get("add_to_db"):
            self.sql_client.add_user(
                name=user["name"], surname=user["surname"], middle_name=user["middle_name"],
                username=user["username"], password=user["password"], email=user["email"]
            )
        # Send request
        # Added "repeat" value to check if user can't be blocked twice in a row
        response = self.api_client.unblock_user(
            method=method, path=f"/api/user/{user['username']}/accept",
            expected_status=expected_status, repeat=user.get("repeat", 1)
        )
        # Check 'status' of response & value of "access" field in database if expected status is 200
        if expected_status == 200:
            assert response.json()['status'] == 'ok', \
                f"Expected 'ok' status, got '{response.json()['status']}'"
            user_mysql = self.sql_client.get_user(username=user["username"])
            assert user_mysql.access == 1
