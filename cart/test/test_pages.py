from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from seleniumlogin import force_login

from cart.models import Cart
from test.factories import TeaFactory, UserFactory

import test.selenium_setup as setup


class TestCartAddPage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(
            firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH),
            executable_path=setup.DRIVER_PATH,
        )
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_cart_add_page(self):
        user = UserFactory.create()
        TeaFactory.create()
        force_login(user, self.selenium, self.live_server_url)

        url = reverse("tea_detail", args=[1])
        self.selenium.get(self.live_server_url + url)
        cart_add_button = self.selenium.find_element(By.ID, "cart-submit")
        cart_add_button.click()

        self.assertEqual(1, User.objects.first().cart_set.first().id)


class TestCartPage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(
            firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH),
            executable_path=setup.DRIVER_PATH,
        )
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self) -> None:
        tea = TeaFactory.create()
        self.user = UserFactory.create()
        Cart.objects.create(product=tea, user=self.user, amount=10)
        self.url = reverse("cart")

    def test_cart_page(self):
        force_login(self.user, self.selenium, self.live_server_url)
        self.selenium.get(self.live_server_url + self.url)

        rows = self.selenium.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(len(rows), 2)

    def test_cart_remove_page(self):
        force_login(self.user, self.selenium, self.live_server_url)
        self.selenium.get(self.live_server_url + self.url)

        remove_button = self.selenium.find_element(
            By.CSS_SELECTOR, "td button:last-of-type"
        )
        remove_button.click()
        self.assertTrue("Пусто" in self.selenium.page_source)

        self.assertEqual(len(Cart.objects.all()), 0)
