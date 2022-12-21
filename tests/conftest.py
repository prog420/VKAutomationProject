import os
import sys
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app.sql.client import MySQLClient
from utils.mock_api import MockAPIClient


def pytest_addoption(parser: pytest.Parser):
    """
    CLI options for pytest launch
    """
    parser.addoption("--browser", default="chrome")
    parser.addoption("--headless", action="store_true", help="Run driver in headless mode.")
    parser.addoption("--selenoid", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--video", action="store_true")
    parser.addoption("--log_dir", default="/tmp/tests")


def pytest_configure(config):
    """
    Set up required clients before the start
    """
    sql_client = MySQLClient(user="root", password="root", db_name="vk_db")
    sql_client.connect(db_created=True)
    if not hasattr(config, "workerinput"):
        # Clean table before the tests
        sql_client.truncate(table="test_users")
        # Add root user
        sql_client.add_user(
            name="Root", surname="User", middle_name="M", username="RootUser", password="RootPass",
            email="root@mail.ru", access=1
        )
    config.sql_client = sql_client

    mock_client = MockAPIClient(host="localhost", port="8083")
    config.mock_client = mock_client
    # Configure paths for logs & screenshots


@pytest.fixture(scope="session")
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope="function")
def test_dir(request: pytest.FixtureRequest, config):
    """
    Get log path for each test
    """
    test_dir = os.path.join(config["log_dir"], request._pyfuncitem.nodeid)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope="session")
def sql_client(request: pytest.FixtureRequest) -> MySQLClient:
    sql_client: MySQLClient = request.config.sql_client
    yield sql_client
    sql_client.connection.close()


@pytest.fixture(scope="session")
def mock_client(request: pytest.FixtureRequest) -> MockAPIClient:
    mock_client: MySQLClient = request.config.mock_client
    yield mock_client


@pytest.fixture(scope="session")
def config(request: pytest.FixtureRequest):
    log_dir = request.config.getoption("--log_dir")
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    vnc = True if request.config.getoption("--vnc") else False
    video = True if request.config.getoption("--video") else False

    if request.config.getoption("--selenoid"):
        selenoid = "http://127.0.0.1:4444/wd/hub"
    else:
        selenoid = None
        vnc = False
        video = False

    chrome_options = Options()
    chrome_options.headless = headless
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--ignore-certificate-errors")
    # Remove "Save password" popup
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    # Remove "Controlled by automated software" info
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

    chrome_options.set_capability("browserName", browser)
    if browser == "chrome":
        chrome_options.set_capability("browserVersion", "chrome_106.0_VNC")
    chrome_options.set_capability("acceptInsecureCerts", True)
    chrome_options.set_capability("sessionTimeout", "2m")
    chrome_options.set_capability(
        "selenoid:options",
        {
            "enableVNC": vnc,
            "enableVideo": video
        }
    )
    return {
        "browser": browser,
        "options": chrome_options,
        "selenoid": selenoid,
        "vnc": vnc,
        "video": video,
        "log_dir": log_dir
    }


@pytest.fixture()
def driver(config):
    selenoid = config["selenoid"]
    browser = config["browser"]

    if selenoid:
        browser = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            options=config["options"]
        )
    elif browser == "chrome":
        browser = webdriver.Chrome(
            options=config["options"],
            service=Service(ChromeDriverManager(version="108.0.5359.71").install())
        )

    yield browser
    browser.quit()
