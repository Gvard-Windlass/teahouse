from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


FIREFOX_BINARY_PATH = "C:\\Program Files\\Firefox Developer Edition\\firefox.exe"
DRIVER_PATH = "C:\\Dev\\django_dev_1\\geckodriver.exe"


class SeleniumWithFirefox(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(
            firefox_binary=FirefoxBinary(FIREFOX_BINARY_PATH),
            executable_path=DRIVER_PATH,
        )
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
