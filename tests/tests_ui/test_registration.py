import json
import allure
import pytest

from app.ui.locators import RegPageLocators
from tests_ui.base_case import BaseCase


@allure.epic("UI")
@allure.feature("Registration Page")
class TestRegistration(BaseCase):
    base_user = {
        "name": "A",
        "surname": "B",
        "middle_name": "C",
        "username": "BaseUser",
        "email": "baseuser@mail.ru",
        "password": "123456",
        "confirm_password": "123456",
        "remove_client_validation": False
    }

    @pytest.mark.UI
    def guest_can_go_to_login_page(self):
        login_page = self.reg_page.go_to_login_page()
        login_page.is_login_page_opened()

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "locator, placeholder",
        [
            (RegPageLocators.NAME_INPUT, "Name"),
            (RegPageLocators.SURNAME_INPUT, "Surname"),
            (RegPageLocators.MIDDLE_NAME_INPUT, "Middle name"),
            (RegPageLocators.USERNAME_INPUT, "Username"),
            (RegPageLocators.EMAIL_INPUT, "Email"),
            (RegPageLocators.PASS_INPUT, "Password"),
            (RegPageLocators.CONFIRM_PASS_INPUT, "Repeat password")
        ],
        ids=[
            "Name input has placeholder 'Name'",
            "Surname input has placeholder 'Surname'",
            "Middle name input has input 'Middle name'",
            "Username input has input 'Username'",
            "Email input has input 'Email'",
            "Password input has placeholder 'Password'",
            "Confirm pass input has placeholder 'Repeat password'"
        ]
    )
    def test_input_has_correct_placeholder(self, locator, placeholder,
                                           request: pytest.FixtureRequest):
        """
        Test if input field have correct placeholder
        """
        allure.dynamic.title(request.node.callspec.id)
        self.reg_page.open()
        input_field = self.reg_page.find(locator)
        actual_placeholder = input_field.get_attribute("placeholder")
        assert actual_placeholder == placeholder, \
            f"Expected placeholder='{placeholder}', got placeholder='{actual_placeholder}'"

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "locator, minlength, maxlength",
        [
            (RegPageLocators.SURNAME_INPUT, "1", "45"),
            (RegPageLocators.USERNAME_INPUT, "6", "16"),
            (RegPageLocators.PASS_INPUT, "6", "255"),
            (RegPageLocators.CONFIRM_PASS_INPUT, "6", "255")
        ],
        ids=[
            "Surname input has min and maxlength",
            "Username input has min and maxlength",
            "Password input has min and maxlength",
            "ConfirmPassword input has min and maxlength"
        ]
    )
    def test_input_has_min_and_max_length(self, locator, minlength, maxlength,
                                          request: pytest.FixtureRequest):
        """
        Test if input field have 'minlength' and 'maxlength' parameters
            MySQL restrictions:
            username: 16 not null
            password: 255 not null
        """
        allure.dynamic.title(request.node.callspec.id)
        self.reg_page.open()
        input_field = self.reg_page.find(locator)
        actual_minlength = input_field.get_attribute("minlength")
        actual_maxlength = input_field.get_attribute("maxlength")
        assert (actual_minlength, actual_maxlength) == (minlength, maxlength), \
            f"Expected minlength={minlength} and maxlength={maxlength}, " \
            f"got minlength={actual_minlength} and maxlength={actual_maxlength}"

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "locator, field",
        [
            (RegPageLocators.NAME_INPUT, "Name"),
            (RegPageLocators.SURNAME_INPUT, "Surname"),
            (RegPageLocators.USERNAME_INPUT, "Username"),
            (RegPageLocators.EMAIL_INPUT, "Email"),
            (RegPageLocators.PASS_INPUT, "Password"),
            (RegPageLocators.CONFIRM_PASS_INPUT, "Repeat password")
        ],
        ids=[
            "Name input has attribute 'required'",
            "Surname input has attribute 'required'",
            "Username input has attribute 'required'",
            "Email input has attribute 'required'",
            "Password input has attribute 'required'",
            "Repeat password input has attribute 'required'",
        ]
    )
    def test_input_has_attribute_required(self, locator, field, request: pytest.FixtureRequest):
        """
        Test if input field has attribute 'required'
        """
        allure.dynamic.title(request.node.callspec.id)
        self.reg_page.open()
        input_field = self.reg_page.find(locator)
        assert input_field.get_property("required"), \
            f"Field '{field}' expected to be required, but it's not required to be filled"

    @pytest.mark.UI
    @allure.title("Guest can register new user with correct data")
    def test_guest_can_register_new_user(self):
        """
        Test is guest can register new user
        """
        user = self.base_user.copy()
        user["username"] = "CorrectReg"
        user["email"] = "correctreg@mail.ru"
        vk_id = "0000"
        self.mock_client.add_user(username=user["username"], vk_id=vk_id)
        self.reg_page.open()
        self.reg_page.register_user(**user)
        assert self.main_page.is_main_page_opened()

    @pytest.mark.UI
    @allure.title("Guest can register new user without middle name")
    def test_guest_can_register_new_user_without_middle_name(self):
        """
        Test is guest can register new user without middle name
        """
        user = self.base_user.copy()
        user["username"] = "NoMiddleName"
        user["email"] = "nomiddlename@mail.ru"
        user["middle_name"] = None
        vk_id = "NoMiddleNameVK_ID"
        self.mock_client.add_user(username=user["username"], vk_id=vk_id)
        self.reg_page.open()
        self.reg_page.register_user(**user)
        assert self.main_page.is_main_page_opened()

    @pytest.mark.UI
    @allure.title("Guest can't register new user with long password")
    def test_guest_cant_register_new_user_with_long_password(self):
        """
        Test is guest can't register new user with password > 255 symbols
        """
        user = self.base_user.copy()
        user["username"] = "LongPassUI"
        user["password"] = "1" * 300
        user["confirm_password"] = user["password"]
        vk_id = "0000"
        self.mock_client.add_user(username=user["username"], vk_id=vk_id)
        self.reg_page.open()
        self.reg_page.register_user(**user)
        alert = self.reg_page.find(self.reg_page.locators.WARNING_MESSAGE)
        self.reg_page.actions.pause(1).perform()
        assert not alert.text == "Internal Server Error"

    @pytest.mark.UI
    @allure.title("Guest can't register new user with empty email and different passwords")
    def test_guest_cant_use_empty_email_and_diff_passwords(self):
        """
        Test is guest can't register new user with empty email and different passwords
        """
        user = self.base_user.copy()
        user["username"] = "EmptyEmailUI"
        user["email"] = ""
        user["password"] = "123456"
        user["confirm_password"] = "654321"
        vk_id = "0000"
        self.mock_client.add_user(username=user["username"], vk_id=vk_id)
        self.reg_page.open()
        self.reg_page.register_user(**user)
        alert = self.reg_page.find(self.reg_page.locators.WARNING_MESSAGE)
        self.reg_page.actions.pause(1).perform()
        # Check if alert message contain raw json data
        alert_text = alert.text.replace("\'", "\"")
        try:
            alert_data = json.loads(alert_text)
        except json.decoder.JSONDecodeError:
            alert_data = alert_text
        assert not isinstance(alert_data, dict), f"Got raw json data as alert message: {alert_text}"
