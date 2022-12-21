""" Locators for all pages. """
from selenium.webdriver.common.by import By


class BasePageLocators:
    """
    Default Locators
    """
    WARNING_MESSAGE = (By.XPATH, '//div[contains(@class, "uk-alert uk-alert")]')


class LoginPageLocators(BasePageLocators):
    """
    Locators for Login Page
    """
    LOGIN_INPUT = (By.XPATH, '//input[@id="username"]')
    PASS_INPUT = (By.XPATH, '//input[@id="password"]')
    SUBMIT_LOGIN = (By.XPATH, '//input[@id="submit"]')
    REG_PAGE_LINK = (By.XPATH, '//a[@href="/reg"]')
    WARNING_MESSAGE = (By.XPATH, '//div[contains(@class, "uk-alert uk-alert")]')


class RegPageLocators(BasePageLocators):
    """
    Locators for Registration Page
    """
    NAME_INPUT = (By.XPATH, '//input[@name="name"]')
    SURNAME_INPUT = (By.XPATH, '//input[@name="surname"]')
    MIDDLE_NAME_INPUT = (By.XPATH, '//input[@name="middlename"]')
    USERNAME_INPUT = (By.XPATH, '//input[@name="username"]')
    EMAIL_INPUT = (By.XPATH, '//input[@name="email"]')
    PASS_INPUT = (By.XPATH, '//input[@name="password"]')
    CONFIRM_PASS_INPUT = (By.XPATH, '//input[@name="confirm"]')
    CHECKBOX_INPUT = (By.XPATH, '//input[@name="term"]')
    SUBMIT_BUTTON = (By.XPATH, '//input[@name="submit"]')
    LOGIN_PAGE_LINK = (By.XPATH, '//a[@href="/login"]')


class MainPageLocators(BasePageLocators):
    """
    Locators for Main Page
    """
    LOGOUT_BTN = (By.XPATH, '//div[@id="logout"]/a')
    API_IMAGE = (By.XPATH, '//img[@src="/static/images/laptop.png"]')
    INTERNET_IMAGE = (By.XPATH, '//img[@src="/static/images/loupe.png"]')
    SMTP_IMAGE = (By.XPATH, '//img[@src="/static/images/analytics.png"]')
