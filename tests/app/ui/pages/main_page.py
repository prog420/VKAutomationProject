from app.ui.pages.base_page import BasePage
from app.ui.locators import MainPageLocators


class MainPage(BasePage):
    path = "/welcome/"
    url = BasePage.url + path
    locators = MainPageLocators()

    def is_main_page_opened(self):
        return self.is_element_present(self.locators.LOGOUT_BTN)

    def is_images_vertically_aligned(self):
        loc_one = self.get_item_location(self.locators.API_IMAGE)
        loc_two = self.get_item_location(self.locators.INTERNET_IMAGE)
        loc_three = self.get_item_location(self.locators.SMTP_IMAGE)
        return loc_one["y"] == loc_two["y"] == loc_three["y"]
