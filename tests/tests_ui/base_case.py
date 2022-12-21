import os.path

import allure
import pytest
import requests

from app.ui.pages.login_page import LoginPage
from app.ui.pages.reg_page import RegPage
from app.ui.pages.main_page import MainPage


class BaseCase:
    driver = None
    sql_client = None
    mock_client = None

    login_page = None
    reg_page = None
    main_page = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, sql_client, mock_client):
        self.driver = driver
        self.sql_client = sql_client
        self.mock_client = mock_client

        self.login_page = LoginPage(self.driver)
        self.reg_page = RegPage(self.driver)
        self.main_page = MainPage(self.driver)

    @pytest.fixture(scope="function", autouse=True)
    def ui_report(self, driver, request: pytest.FixtureRequest, test_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(test_dir, "browser.log")
            with open(browser_logs, "w") as f:
                for i in driver.get_log("browser"):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(test_dir, "failed.png")
            self.driver.save_screenshot(filename=screenshot_path)
            allure.attach.file(screenshot_path, "failed.png", allure.attachment_type.PNG)
            with open(browser_logs, "r") as f:
                allure.attach(f.read(), "test.log", allure.attachment_type.TEXT)
