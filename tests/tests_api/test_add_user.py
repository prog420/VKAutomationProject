import json
import allure
import pytest
from tests_api.base_case import BaseAPICase
from test_data.api_data import APIData


@allure.epic("API")
@allure.feature("/api/user - Add New User")
class TestAddUserAPI(BaseAPICase):
    @pytest.mark.API
    @pytest.mark.parametrize(
        "title, test_case_link, data, content_type, expected_status",
        [test_case["case"] for test_case in APIData.add_user_data],
        ids=[test_case["case"][0] for test_case in APIData.add_user_data]
    )
    def test_adding_user(self, title, test_case_link, data, content_type, expected_status):
        """
        Parametrized test for /api/user POST request
        :param title: name of the test
        :param test_case_link: link to test documented in Notion
        :param data: payload for request
        :param content_type: content type of request body
        :param expected_status: Expected status code
        """
        allure.dynamic.title(title)
        allure.dynamic.link(test_case_link, name='Test Case')
        response = self.api_client.add_user(
            data=json.dumps(data), content_type=content_type, expected_status=expected_status
        )
        # If user must be added, check user in database. Skip for negative checks
        if expected_status == 201:
            assert self.sql_client.get_user(username=data["username"])

    @pytest.mark.API
    @allure.title("Unauthorized user can't use Add User request")
    @allure.link('https://www.notion.so/593d3ebb6c104c388288d806e063630f', name='Test Case')
    def test_unauthorized_user_cant_use_api_requests(self):
        """
        Test if unauthorized user can send Add User API request. Expected status: 401 Unauthorized
        """
        data = {
            "name": "Name", "surname": "Surname", "username": "NoAuthUser",
            "password": "qwerty123", "email": "noauthuser@mail.ru"
        }
        response = self.api_client_no_auth.add_user(
            data=json.dumps(data), content_type='application/json', expected_status=401
        )

    @pytest.mark.API
    @allure.title("Two similar users can't be created")
    @allure.link('https://www.notion.so/1f389da1d7b447b693cb71cfca684fc5', name='Test Case')
    def test_duplicate_user_cant_be_created(self):
        """
        Test if two similar users can be created. Expected: status 400 (OR 409?)
        """
        data = {
            "name": "Name", "surname": "Surname", "username": "DuplicateUser",
            "password": "ABC12346", "email": "clone@mail.ru"
        }
        self.api_client.add_user(
            data=json.dumps(data), content_type='application/json'
        )
        response = self.api_client.add_user(
            data=json.dumps(data), content_type='application/json', expected_status=400
        )

    @pytest.mark.API
    @allure.title("Duplicate emails can't be used")
    @allure.link('https://www.notion.so/email-06c85a8a7f2d41229a85e098ac411da8', name='Test Case')
    def test_duplicate_email_cant_be_used(self):
        """
        Test if two users can be created with one email but different logins. Expected status: 400
        """
        data = {
            "name": "Name", "surname": "Surname", "username": "DuplicateEmail_1",
            "password": "Abc12346", "email": "clone@mail.ru"
        }
        self.api_client.add_user(
            data=json.dumps(data), content_type='application/json'
        )
        data["username"] = "DuplicateEmail_2"
        response = self.api_client.add_user(
            data=json.dumps(data), content_type='application/json', expected_status=400
        )

    @pytest.mark.API
    @allure.title("Wrong method can't be used")
    @allure.link('https://www.notion.so/POST-91d2cddf42d54f179cd7e0238f7063e8', name='Test Case')
    def test_wrong_method_cant_be_used(self):
        """
        Test if another methods can be used. Expected status: 400
        """
        data = {
            "name": "Name", "surname": "Surname", "username": "MethodUser",
            "password": "ABC12346", "email": "method@mail.ru"
        }
        response = self.api_client.add_user(
            method="GET", data=json.dumps(data), content_type='application/json'
        )
