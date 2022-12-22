from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from catalogue.models import Tea
from test.factories import TeaFactory

import test.selenium_setup as setup

class TestHomePage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH), executable_path=setup.DRIVER_PATH)
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


class TestProductsDisplay(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH), executable_path=setup.DRIVER_PATH)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    
    def test_tea_display(self):
        TeaFactory.create_batch(2)

        url = reverse('products_all')
        self.selenium.get(self.live_server_url+url)
        tea_products = self.selenium.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(tea_products), 2)


class TestProductDetailPage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH), executable_path=setup.DRIVER_PATH)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_tea_detail_page(self):
        tea = TeaFactory.create()

        url = reverse('tea_detail', args=[tea.id])
        self.selenium.get(self.live_server_url+url)
        amount_imput = self.selenium.find_element(By.CSS_SELECTOR, 'input[name=amount]')
        total_display = self.selenium.find_element(By.ID, 'total')
        initial_total = total_display.text

        move = ActionChains(self.selenium)
        
        move.click_and_hold(amount_imput).move_by_offset(10, 0).release().perform()
        self.assertNotEqual(initial_total, total_display.text)


class TestHomePage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH), executable_path=setup.DRIVER_PATH)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_tea_detail_page(self):
        TeaFactory.create_batch(2)

        self.selenium.get(f'{self.live_server_url}/')

        search_input = self.selenium.find_element(By.NAME, 'q')
        current_url = self.selenium.current_url

        search_input.send_keys('test tea')
        search_input.send_keys(Keys.RETURN)

        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        products = self.selenium.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(products), 2)