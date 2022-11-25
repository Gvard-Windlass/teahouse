from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from catalogue.models import Tea

firefox_dev_binary = FirefoxBinary('C:\Program Files\Firefox Developer Edition\\firefox.exe')
driver_path = 'C:\Dev\django_dev_1\geckodriver.exe'

class TestHomePage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_sidebar_small_screen(self):
        self.selenium.get(f'{self.live_server_url}/')
        self.selenium.set_window_size(width=700, height=500)

        sidebar_toggle = self.selenium.find_element(By.ID, 'sidebarToggle')
        sidebar = self.selenium.find_element(By.ID, 'productLinks')

        self.assertFalse(sidebar.is_displayed())
        sidebar_toggle.click()
        self.assertTrue(sidebar.is_displayed())


    def test_sidebar_big_screen(self):
        self.selenium.get(f'{self.live_server_url}/')
        self.selenium.set_window_size(width=1000, height=500)
        
        sidebar_toggle = self.selenium.find_element(By.ID, 'sidebarToggle')
        sidebar = self.selenium.find_element(By.ID, 'productLinks')
        
        self.assertFalse(sidebar_toggle.is_displayed())
        self.assertTrue(sidebar.is_displayed())


class TestProductDisplay(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    
    def test_tea_display(self):
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

        Tea.objects.create(
            name='test tea 2',
            price = 200.5,
            image = 'product_images/black2.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2021,
            tea_amount = 50.5
        )

        self.selenium.get(f'{self.live_server_url}/tea/')
        tea_products = self.selenium.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(tea_products), 2)
