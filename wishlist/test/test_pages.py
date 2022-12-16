from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from django.test import Client
from django.contrib.auth.models import User

from seleniumlogin import force_login

from catalogue.models import Tea

firefox_dev_binary = FirefoxBinary('C:\Program Files\Firefox Developer Edition\\firefox.exe')
driver_path = 'C:\Dev\django_dev_1\geckodriver.exe'

class TestWishlistToggle(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    
    def test_wishlist_toggle(self):
        Tea.objects.create(
            name='test tea 1',
            price = 300.5,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            tea_amount = 300.5
        )

        self.selenium.get(f'{self.live_server_url}/product_catalogue/')
        wishlist_button = self.selenium.find_element(By.CLASS_NAME, 'btnWishlist')
        self.assertEqual(wishlist_button.text, '♡')
        wishlist_button.click()
        self.assertEqual(wishlist_button.text, '♥')


class TestWishlistPage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    
    def test_wishlist_page_anonymous(self):
        Tea.objects.create(
            name='test tea 1',
            price = 300.5,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            tea_amount = 300.5
        )

        self.selenium.get(f'{self.live_server_url}/product_catalogue/')
        wishlist_button = self.selenium.find_element(By.CLASS_NAME, 'btnWishlist')
        self.assertEqual(wishlist_button.text, '♡')
        wishlist_button.click()

        self.selenium.get(f'{self.live_server_url}/wishlist_display/')
        tea_products = self.selenium.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(tea_products), 1)


    def test_wishlist_page_authenticated(self):
        Tea.objects.create(
            name='test tea 1',
            price = 300.5,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            tea_amount = 300.5
        )

        user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        force_login(user, self.selenium, self.live_server_url)
        
        self.selenium.get(f'{self.live_server_url}/product_catalogue/')
        wishlist_button = self.selenium.find_element(By.CLASS_NAME, 'btnWishlist')
        self.assertEqual(wishlist_button.text, '♡')
        wishlist_button.click()

        self.selenium.get(f'{self.live_server_url}/wishlist_display/')
        tea_products = self.selenium.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(tea_products), 1)