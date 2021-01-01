import os

# Ref: https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html?highlight=implicitly#selenium.webdriver.remote.webdriver.WebDriver.implicitly_wait
SELENIUM_TIME_TO_WAIT_IN_SECONDS = 5

DC_POSTING_DELAY_IN_SECONDS = 1

# Ref: https://chromedriver.storage.googleapis.com/index.html
CHROME_DRIVER_VERSION = "87.0.4280.88"
CHROME_DRIVER_FILENAME_LINUX = "chromedriver_linux64.zip"
CHROME_DRIVER_FILENAME_MAC = "chromedriver_mac64.zip"
CHROME_DRIVER_FILENAME_WINDOWS = "chromedriver_win32.zip"
CHROME_DRIVER_ZIPCONTENT_FILENAME = "chromedriver"

CHROME_DRIVER_URL_ROOT = "https://chromedriver.storage.googleapis.com"
CHROME_DRIVER_URL_LINUX = f"{CHROME_DRIVER_URL_ROOT}/{CHROME_DRIVER_VERSION}/{CHROME_DRIVER_FILENAME_LINUX}"
CHROME_DRIVER_URL_MAC = f"{CHROME_DRIVER_URL_ROOT}/{CHROME_DRIVER_VERSION}/{CHROME_DRIVER_FILENAME_MAC}"
CHROME_DRIVER_URL_WINDOWS = f"{CHROME_DRIVER_URL_ROOT}/{CHROME_DRIVER_VERSION}/{CHROME_DRIVER_FILENAME_WINDOWS}"

DCBOT_PACKAGE_DIRPATH = os.path.dirname(__file__)
CHROME_DRIVER_INSTALL_DIRPATH = os.path.join(DCBOT_PACKAGE_DIRPATH, "driver")
CHROME_DRIVER_INSTALL_PATH = os.path.join(
    CHROME_DRIVER_INSTALL_DIRPATH, f"{CHROME_DRIVER_ZIPCONTENT_FILENAME}_{CHROME_DRIVER_VERSION}"
)
