import allure
import pytest
from tests_api.base_case import BaseAPICase
from test_data.api_data import APIData


@allure.epic("API")
@allure.feature("/api/user/<username> - Delete User")
class TestDeleteUserAPI(BaseAPICase):
    @pytest.mark.API
    @pytest.mark.parametrize(
        "title, test_case_link, user, method, expected_status",
        [test_case["case"] for test_case in APIData.delete_user_data],
        ids=[test_case["case"][0] for test_case in APIData.delete_user_data]
    )
    def test_delete_user(self, title, test_case_link, user, method, expected_status):
        """
        Test if user can be deleted
        :param title: name of the test
        :param test_case_link: link to test documented in Notion
        :param user: User data for database
        :param method: HTTP method for request
        :param expected_status: Expected status code
        :return:
        """
        allure.dynamic.title(title)
        allure.dynamic.link(test_case_link, name='Test Case')
        # Add User to database if needed
        if user["add_to_db"]:
            self.sql_client.add_user(
                name=user["name"], surname=user["surname"], middle_name=user["middle_name"],
                username=user["username"], password=user["password"], email=user["email"]
            )
        # Send request
        response = self.api_client.delete_user(
            method=method, path=f"/api/user/{user['username']}", expected_status=expected_status
        )
        # Check if user was deleted from database if expected status is 204
        if expected_status == 204:
            user = self.sql_client.get_user(username=user["username"])
            assert not user
