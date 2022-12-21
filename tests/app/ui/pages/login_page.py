from app.ui.pages.base_page import BasePage
from app.ui.pages.main_page import MainPage
from app.ui.locators import LoginPageLocators


class LoginPage(BasePage):

    locators = LoginPageLocators()

    def is_login_page_opened(self):
        return self.is_element_present(self.locators.LOGIN_INPUT)

    def authorize(self, username="DmitryBV", password="123456") -> MainPage:
        self.find(self.locators.LOGIN_INPUT).send_keys(username)
        self.find(self.locators.PASS_INPUT).send_keys(password)
        self.find(self.locators.SUBMIT_LOGIN).click()
        return MainPage(self.driver)

    def go_to_registration_page(self):
        reg_page_link = self.locators.REG_PAGE_LINK
        self.find_clickable_element(locator=reg_page_link).click()
