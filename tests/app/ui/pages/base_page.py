import subprocess
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from app.ui.locators import BasePageLocators


class BasePage:
    # Get APP url
    app_container_name = "app"
    docker_inspect = "docker inspect -f '{{range.NetworkSettings.Networks}}" \
                     "{{.IPAddress}}{{end}}' " + app_container_name
    app_ip = subprocess.check_output(docker_inspect, shell=True)
    app_ip = app_ip.decode().strip()
    url = f"http://{app_ip}:8082"

    locators = BasePageLocators()

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.actions = ActionChains(driver)

    def open(self):
        self.driver.get(self.url)

    def wait(self, timeout=None) -> WebDriverWait:
        """
        Basic setup for Explicit Waits
        :param timeout: max time (in seconds) to wait for condition
        :return: WebDriverWait
        """
        if timeout is None:
            timeout = 10
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None) -> WebElement:
        """
        Find element by its locator
        :param locator: (by, selector)
        :param timeout: max time (in seconds) to wait for condition
        :return: WebElement
        """
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_clickable_element(self, locator, timeout=None) -> WebElement:
        """
        Find element by its locator
        :param locator: (by, selector)
        :param timeout: max time (in seconds) to wait for condition
        :return: WebElement
        """
        return self.wait(timeout).until(EC.element_to_be_clickable(locator))

    def find_visible_element(self, locator, timeout=None) -> WebElement:
        """
        Find element by its locator
        :param locator: (by, selector)
        :param timeout: max time (in seconds) to wait for condition
        :return: WebElement
        """
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def is_element_present(self, locator, timeout=None) -> bool:
        """
        Check if element is present on a page.
        :param locator: (by, what)
        :param timeout: maximum time (in seconds) to wait for condition
        :return: bool
        """
        try:
            self.find(locator=locator, timeout=timeout)
        except TimeoutException:
            return False
        return True

    def is_not_element_present(self, locator, timeout=None):
        """
        Check if element is not present on a page.
        :param locator: (by, what)
        :param timeout: maximum time (in seconds) to wait for condition
        :return: bool
        """
        try:
            self.find(locator=locator, timeout=timeout)
        except TimeoutException:
            return True
        return False

    def get_item_location(self, locator, timeout=None) -> WebElement.location:
        """
        Get x, y coordinates of element
        :param locator: locator if the element
        :param timeout: timeout of search
        :return: dict
        """
        element = self.find(locator=locator, timeout=timeout)
        return element.location
