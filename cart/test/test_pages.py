from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from seleniumlogin import force_login

from catalogue.models import Tea
from cart.models import Cart

firefox_dev_binary = FirefoxBinary('C:\Program Files\Firefox Developer Edition\\firefox.exe')
driver_path = 'C:\Dev\django_dev_1\geckodriver.exe'

class TestCartAddPage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_cart_add_page(self):
        user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
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
        force_login(user, self.selenium, self.live_server_url)

        self.selenium.get(f'{self.live_server_url}/tea/1/')
        cart_add_button = self.selenium.find_element(By.ID, 'cart-add-button')
        cart_add_button.click()

        self.assertEqual(1, User.objects.first().cart_set.first().id)