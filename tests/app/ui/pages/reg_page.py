from app.ui.pages.base_page import BasePage
from app.ui.locators import RegPageLocators


class RegPage(BasePage):
    path = "/reg"
    url = BasePage.url + path
    locators = RegPageLocators()

    def is_reg_page_opened(self):
        return self.is_element_present(self.locators.NAME_INPUT)

    def go_to_login_page(self):
        login_page_link = self.locators.LOGIN_PAGE_LINK
        self.find_clickable_element(locator=login_page_link).click()

    def register_user(self, name=None, surname=None, middle_name=None, username=None, email=None,
                      password=None, confirm_password=None, remove_client_validation=False,
                      click_checkbox=True):
        """
        Register user with or without client-side input validation
        """
        user_data = [
            (self.locators.NAME_INPUT, name),
            (self.locators.SURNAME_INPUT, surname),
            (self.locators.MIDDLE_NAME_INPUT, middle_name),
            (self.locators.USERNAME_INPUT, username),
            (self.locators.EMAIL_INPUT, email),
            (self.locators.PASS_INPUT, password),
            (self.locators.CONFIRM_PASS_INPUT, confirm_password)
        ]
        # Iterate through user fields in send text if needed
        for locator, text in user_data:
            if text is not None:
                input_field = self.find(locator)
                if remove_client_validation:
                    self.driver.execute_script(
                        'arguments[0].removeAttribute("maxlength")', input_field
                    )
                    self.driver.execute_script(
                        'arguments[0].removeAttribute("minlength")', input_field
                    )
                    self.driver.execute_script(
                        'arguments[0].removeAttribute("required")', input_field
                    )
                input_field.clear()
                input_field.send_keys(text)
        # Click checkbox is click_checkbox is True
        if click_checkbox:
            self.find(locator=self.locators.CHECKBOX_INPUT).click()
        self.find(locator=self.locators.SUBMIT_BUTTON).click()
