from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from seleniumlogin import force_login

from cart.models import Cart
from test.factories import TeaFactory, UserFactory

from test.selenium_setup import SeleniumWithFirefox


class TestCartAddPage(SeleniumWithFirefox):
    def test_cart_add_page(self):
        user = UserFactory.create()
        TeaFactory.create()
        force_login(user, self.selenium, self.live_server_url)

        url = reverse("tea_detail", args=[1])
        self.selenium.get(self.live_server_url + url)
        cart_add_button = self.selenium.find_element(By.ID, "cart-submit")
        cart_add_button.click()

        self.assertEqual(1, User.objects.first().cart_set.first().id)


class TestCartPage(SeleniumWithFirefox):
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
