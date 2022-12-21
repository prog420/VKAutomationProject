import json
import allure
import pytest
from tests_api.base_case import BaseAPICase
from test_data.api_data import APIData


@allure.epic("API")
@allure.feature("/api/user/<username>/change-password - Change Password")
class TestChangePasswordAPI(BaseAPICase):
    @pytest.mark.API
    @pytest.mark.parametrize(
        "title, test_case_link, user, method, content_type, expected_status",
        [test_case["case"] for test_case in APIData.change_password_data],
        ids=[test_case["case"][0] for test_case in APIData.change_password_data]
    )
    def test_change_password(self, title, test_case_link, user, method,
                             content_type, expected_status):
        """
        Parametrized test if password of a user can be changed
        :param title: name of the test
        :param test_case_link: link to test documented in Notion
        :param user: User data for database
        :param method: HTTP method for request
        :param content_type: content type of request body
        :param expected_status: Expected status code
        """
        allure.dynamic.title(title)
        allure.dynamic.link(test_case_link, name='Test Case')
        # Add User to database if needed
        if user.get("add_to_db"):
            self.sql_client.add_user(
                name=user["name"], surname=user["surname"], middle_name=user["middle_name"],
                username=user["username"], password=user["password"], email=user["email"]
            )
        # Send request
        data = {"password": user["new_password"]}
        response = self.api_client.change_password(
            method=method, path=f"/api/user/{user['username']}/change-password",
            content_type=content_type, data=json.dumps(data), expected_status=expected_status
        )
        # Check value of "password" field in database if expected status is 200
        if expected_status == 200:
            user_mysql = self.sql_client.get_user(username=user["username"])
            assert user_mysql.password == user["new_password"]
