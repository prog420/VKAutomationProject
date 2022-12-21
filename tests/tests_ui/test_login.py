import time
import pytest
import allure

from app.ui.locators import LoginPageLocators
from tests_ui.base_case import BaseCase
from test_data.ui_data import UITestData


@allure.epic("UI")
@allure.feature("Login Page")
class TestLogin(BaseCase):
    @pytest.mark.UI
    @allure.title("Guest can open login page")
    def test_guest_can_open_login_page(self):
        """
        Test if unauthorized user can open login page.
        """
        self.login_page.open()
        assert self.login_page.is_login_page_opened()

    @pytest.mark.UI
    @allure.title("Guest can go from login page to registration page")
    def test_guest_can_go_to_reg_page(self):
        """
        Test if unauthorized user can go to registration page
        """
        self.login_page.open()
        self.login_page.go_to_registration_page()
        assert self.reg_page.is_reg_page_opened()

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "locator, minlength, maxlength",
        [
            (LoginPageLocators.LOGIN_INPUT, "6", "16"),
            (LoginPageLocators.PASS_INPUT, "6", "255")
        ],
        ids=[
            "Username input has min and maxlength",
            "Password input has min and maxlength"
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
        self.login_page.open()
        input_field = self.login_page.find(locator)
        actual_minlength = input_field.get_attribute("minlength")
        actual_maxlength = input_field.get_attribute("maxlength")
        assert (actual_minlength, actual_maxlength) == (minlength, maxlength), \
            f"Expected minlength={minlength} and maxlength={maxlength}, " \
            f"got minlength={actual_minlength} and maxlength={actual_maxlength}"

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "locator, placeholder",
        [
            (LoginPageLocators.LOGIN_INPUT, "Username"),
            (LoginPageLocators.PASS_INPUT, "Password")
        ],
        ids=[
            "Username input has placeholder 'Username'",
            "Password input has placeholder 'Password'"
        ]
    )
    def test_input_has_correct_placeholder(self, locator, placeholder,
                                           request: pytest.FixtureRequest):
        """
        Test if input field have correct placeholder
        """
        allure.dynamic.title(request.node.callspec.id)
        self.login_page.open()
        input_field = self.login_page.find(locator)
        actual_placeholder = input_field.get_attribute("placeholder")
        assert actual_placeholder == placeholder, \
            f"Expected placeholder='{placeholder}', got placeholder='{actual_placeholder}'"

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "locator",
        [LoginPageLocators.LOGIN_INPUT, LoginPageLocators.PASS_INPUT],
        ids=[
            "Username input has attribute 'required'",
            "Password input has attribute 'required'"
        ]
    )
    def test_input_has_attribute_required(self, locator, request: pytest.FixtureRequest):
        """
        Test if input field has attribute 'required'
        """
        allure.dynamic.title(request.node.callspec.id)
        self.login_page.open()
        input_field = self.login_page.find(locator)
        assert input_field.get_property("required"), \
            "Field expected to be required, but it's not required to be filled"

    @pytest.mark.UI
    @allure.title("User with correct credentials can authorize")
    @allure.link("https://www.notion.so/820af7e3cc134f59a8582c7d6516695c", name="Test Case")
    def test_guest_can_authorize(self):
        """
        Test if unauthorized user can authorize with correct credentials
        """
        user = UITestData.correct_user.copy()
        self.sql_client.delete_user(filter_by="email", value=user["email"])
        self.sql_client.add_user(**user)
        self.login_page.open()
        main_page = self.login_page.authorize(username=user["username"], password=user["password"])
        assert main_page.is_main_page_opened(), \
            f"User with '{user['username']}' username " \
            f"and '{user['password']}' pass was not authorized"

    @pytest.mark.UI
    @allure.title("Guest can't authorize with invalid username")
    @allure.link("https://www.notion.so/80db595a114140b994318082f71985b0", name="Test Case")
    def test_guest_cant_authorize_with_invalid_username(self):
        """
        Test if unauthorized user can authorize with invalid username
        [Failed] No symbol validation on username field
        """
        user = UITestData.invalid_username_user.copy()
        self.sql_client.delete_user(filter_by="email", value=user["email"])
        self.sql_client.add_user(**user)
        self.login_page.open()
        main_page = self.login_page.authorize(username=user["username"], password=user["password"])
        assert not main_page.is_main_page_opened(), \
            f"User with invalid '{user['username']}' username was authorized"

    @pytest.mark.UI
    @allure.title("Guest can't authorize with ' ' password")
    @allure.link("https://www.notion.so/a65e6363fa2b46d193ab0de8359197a9", name="Test Case")
    def test_guest_cant_authorize_using_space_as_password(self):
        """
        Test if unauthorized user can authorize with '      ' as a password
        [Failed] Password "      " triggers alert with russian language
        """
        warning_text = "Invalid username or password"
        self.login_page.open()
        self.login_page.authorize(username="RandomUser", password="      ")
        alert = self.login_page.find(self.login_page.locators.WARNING_MESSAGE)
        self.login_page.actions.pause(0.5).perform()
        assert warning_text == alert.text, \
            f"Expected '{warning_text}' alert message, got '{alert.text}'"

    @pytest.mark.UI
    @allure.title("Alert DIV element disappear after 5 seconds")
    @allure.link("https://www.notion.so/314062cedc5846c59cea0725f3312c46", name="Test Case")
    def test_guest_cant_authorize_using_space_as_password(self):
        """
        Test Alert DIV element disappear after 5 seconds
        [Failed] Alert element does not have "display: none" CSS attribute
        """
        self.login_page.open()
        self.login_page.authorize(username="abcdef", password="abcdef")
        alert = self.login_page.find(self.login_page.locators.WARNING_MESSAGE)

        self.login_page.actions.pause(6).perform()
        required_display_attr = "none"
        actual_display_attr = alert.value_of_css_property("display")
        assert actual_display_attr == required_display_attr, \
            f"Expected '{required_display_attr}' display value, got value '{actual_display_attr}'"

    @pytest.mark.UI
    @allure.title("Images on the main page are vertically aligned in narrow browser window")
    def test_if_images_are_vertically_aligned(self):
        """
        TODO: Move to MAIN page tests
        Check if main page images are correctly V aligned
        [Failed] Images with window size ~1000 are not correctly V aligned
        """
        self.driver.set_window_size(1000, 1080)
        self.login_page.open()
        main_page = self.login_page.authorize(username="UIUser", password="123456AQA")
        assert main_page.is_images_vertically_aligned(), \
            "Main page images are not vertically aligned"
