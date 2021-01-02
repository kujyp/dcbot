import os
import shutil
import stat
import time
from sys import platform
from urllib.request import urlretrieve
from zipfile import ZipFile

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from dcbot.config import DCBOT_PACKAGE_DIRPATH, \
    CHROME_DRIVER_ZIPCONTENT_FILENAME, CHROME_DRIVER_INSTALL_DIRPATH, \
    CHROME_DRIVER_INSTALL_PATH, CHROME_DRIVER_URL_LINUX, CHROME_DRIVER_URL_MAC, CHROME_DRIVER_URL_WINDOWS, \
    SELENIUM_TIME_TO_WAIT_IN_SECONDS, SELENIUM_USER_AGENT


def ensure_driver_installed():
    if os.path.exists(CHROME_DRIVER_INSTALL_PATH):
        if os.path.isfile(CHROME_DRIVER_INSTALL_PATH) and os.access(CHROME_DRIVER_INSTALL_PATH, os.X_OK):
            return
        else:
            shutil.rmtree(CHROME_DRIVER_INSTALL_DIRPATH)

    # Ref: https://docs.python.org/3/library/sys.html#sys.platform
    if platform.startswith("linux"):
        url = CHROME_DRIVER_URL_LINUX
    elif platform == "darwin":
        url = CHROME_DRIVER_URL_MAC
    elif platform == "win32" or platform == "cygwin":
        url = CHROME_DRIVER_URL_WINDOWS
    else:
        raise EnvironmentError(f"Not supported OS. [{platform}]")

    filename = url.split("/")[-1]

    driver_dirpath = os.path.join(DCBOT_PACKAGE_DIRPATH, "driver")
    download_path = os.path.join(driver_dirpath, filename)
    if not os.path.isdir(driver_dirpath):
        if os.path.isfile(driver_dirpath):
            print(f"Remove file [{driver_dirpath}]...")
            os.remove(driver_dirpath)
        os.makedirs(driver_dirpath)
    print(f"Download driver [{url}]...")
    _filename, _headers = urlretrieve(url, download_path)
    with ZipFile(download_path, 'r') as zf:
        assert CHROME_DRIVER_ZIPCONTENT_FILENAME in zf.namelist(), \
            f"[{url}] doesn't contain '{CHROME_DRIVER_ZIPCONTENT_FILENAME}' file."
        print(f"Install driver on [{CHROME_DRIVER_INSTALL_DIRPATH}]...")
        zf.extract(CHROME_DRIVER_ZIPCONTENT_FILENAME, CHROME_DRIVER_INSTALL_DIRPATH)
        shutil.move(
            os.path.join(CHROME_DRIVER_INSTALL_DIRPATH, CHROME_DRIVER_ZIPCONTENT_FILENAME),
            CHROME_DRIVER_INSTALL_PATH,
        )

    os.remove(download_path)
    os.chmod(CHROME_DRIVER_INSTALL_PATH, os.stat(CHROME_DRIVER_INSTALL_PATH).st_mode | stat.S_IEXEC)


class WebDriverContainer:
    def __init__(self) -> None:
        ensure_driver_installed()
        print(f"Opening web browser...")
        options = Options()
        options.add_argument(f"user-agent={SELENIUM_USER_AGENT}")
        self.driver = WebDriver(CHROME_DRIVER_INSTALL_PATH, options=options)
        self.driver.implicitly_wait(SELENIUM_TIME_TO_WAIT_IN_SECONDS)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing web browser...")
        self.driver.close()

    def get(self, url: str, print_log: bool = True):
        if print_log:
            print(f"Retrieve url [{url}]...")
        self.driver.get(url)

    def find_element_by_id(self, id_: str):
        WebDriverWait(self.driver, SELENIUM_TIME_TO_WAIT_IN_SECONDS) \
            .until(expected_conditions.presence_of_element_located((By.ID, id_)))
        return self.driver.find_element_by_id(id_)

    def find_element_by_class_name(self, name: str):
        WebDriverWait(self.driver, SELENIUM_TIME_TO_WAIT_IN_SECONDS) \
            .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, name)))
        return self.driver.find_element_by_class_name(name)

    @property
    def current_url(self):
        return self.driver.current_url


class DcBrowser:
    def __init__(self, web_driver_container: WebDriverContainer, dc_nickname: str, dc_article_password: str) -> None:
        self.web_driver_container = web_driver_container
        self.dc_nickname = dc_nickname
        self.dc_article_password = dc_article_password

    # def ensure_signin(self):
    #     if self.is_signed():
    #         return
    #     self.web_driver_container.get("https://m.dcinside.com/auth/login")
    #     element_userid = self.web_driver_container.find_element_by_id("user_id")
    #     element_userid.send_keys(self.dc_account)
    #     element_userpw = self.web_driver_container.find_element_by_id("user_pw")
    #     element_userpw.send_keys(self.dc_password)
    #     element_loginok = self.web_driver_container.find_element_by_id("login_ok")
    #     print("Signing in...")
    #     before_signin_url = self.web_driver_container.current_url
    #     element_loginok.click()
    #
    #     WebDriverWait(self.web_driver_container.driver, SELENIUM_TIME_TO_WAIT_SECONDS) \
    #         .until(lambda driver: driver.current_url != before_signin_url)

    def is_signed(self):
        self.web_driver_container.get("https://m.dcinside.com/aside")
        element_loginbox = self.web_driver_container.find_element_by_class_name("login-box")
        return "로그인 해주세요." not in element_loginbox.text

    def post_article(self, gall_id: str, title: str, content: str):
        self.web_driver_container.get(f"https://gall.dcinside.com/mgallery/board/write/?id={gall_id}")
        element_name = self.web_driver_container.find_element_by_id("name")
        element_name.send_keys(self.dc_nickname)
        element_password = self.web_driver_container.find_element_by_id("password")
        element_password.send_keys(self.dc_article_password)
        element_subject = self.web_driver_container.find_element_by_id("subject")
        element_subject.send_keys(title)
        element_canvas_iframe = self.web_driver_container.find_element_by_id("tx_canvas_wysiwyg")
        self.web_driver_container.driver.switch_to.frame(element_canvas_iframe)
        element_content_container = self.web_driver_container.find_element_by_class_name("tx-content-container")
        element_content_container.send_keys(content)
        self.web_driver_container.driver.switch_to.default_content()
        element_write_btn = self.web_driver_container.driver.find_element_by_class_name("btn_svc")
        element_write_btn.click()


def post(dc_nickname: str, dc_article_password: str, gall_id: str, title: str, content: str):
    with WebDriverContainer() as web_driver_container:
        post_with(web_driver_container, dc_nickname, dc_article_password, gall_id, title, content)


def post_with(
        web_driver_container: WebDriverContainer, dc_nickname: str, dc_article_password: str, gall_id: str, title: str, content: str
):
    dc_browser = DcBrowser(web_driver_container, dc_nickname, dc_article_password)
    # TODO(kujyp 200102 0140): 글쓰기 에러처리하기. 글자수 부족하면 "최소 2자 이상 입력해주십시오." 이런 알람 뜸
    dc_browser.post_article(gall_id, title, content)
    time.sleep(5)
