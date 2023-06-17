from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from test.factories import TeaFactory

from test.selenium_setup import SeleniumWithFirefox


class TestHomePage(SeleniumWithFirefox):
    def test_sidebar_small_screen(self):
        self.selenium.get(f"{self.live_server_url}/")
        self.selenium.set_window_size(width=700, height=500)

        sidebar_toggle = self.selenium.find_element(By.ID, "sidebarToggle")
        sidebar = self.selenium.find_element(By.ID, "productLinks")

        self.assertFalse(sidebar.is_displayed())
        sidebar_toggle.click()
        self.assertTrue(sidebar.is_displayed())

    def test_sidebar_big_screen(self):
        self.selenium.get(f"{self.live_server_url}/")
        self.selenium.set_window_size(width=1000, height=500)

        sidebar_toggle = self.selenium.find_element(By.ID, "sidebarToggle")
        sidebar = self.selenium.find_element(By.ID, "productLinks")

        self.assertFalse(sidebar_toggle.is_displayed())
        self.assertTrue(sidebar.is_displayed())


class TestProductsDisplay(SeleniumWithFirefox):
    def test_tea_display(self):
        TeaFactory.create_batch(2)

        url = reverse("products_all")
        self.selenium.get(self.live_server_url + url)
        tea_products = self.selenium.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(tea_products), 2)

    def test_pagination(self):
        TeaFactory.create_batch(40)

        url = reverse("products_all")
        self.selenium.get(self.live_server_url + url)
        pagination = self.selenium.find_element(By.CLASS_NAME, "pagination")
        self.assertTrue(pagination.is_displayed())

        pg_next = self.selenium.find_element(By.ID, "page-next")
        current_url = self.selenium.current_url
        pg_next.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        pg_end = self.selenium.find_element(By.ID, "page-end")
        current_url = self.selenium.current_url
        pg_end.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        pg_prev = self.selenium.find_element(By.ID, "page-prev")
        current_url = self.selenium.current_url
        pg_prev.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        pg_begin = self.selenium.find_element(By.ID, "page-begin")
        current_url = self.selenium.current_url
        pg_begin.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))


class TestProductsSearch(SeleniumWithFirefox):
    def setUp(self):
        TeaFactory.create_batch(40)

    def test_product_search(self):
        self.selenium.get(f"{self.live_server_url}/")

        query_imput = self.selenium.find_element(By.CSS_SELECTOR, "input[name=q]")
        query_imput.send_keys("tea")

        current_url = self.selenium.current_url
        query_imput.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        tea_products = self.selenium.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(tea_products), 10)

    def test_search_pagination(self):
        url = reverse("product_search")
        q = "tea"
        self.selenium.get(f"{self.live_server_url}{url}?q={q}")

        pagination = self.selenium.find_element(By.CLASS_NAME, "pagination")
        self.assertTrue(pagination.is_displayed())

        pg_next = self.selenium.find_element(By.ID, "page-next")
        current_url = self.selenium.current_url
        pg_next.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        pg_end = self.selenium.find_element(By.ID, "page-end")
        current_url = self.selenium.current_url
        pg_end.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        pg_prev = self.selenium.find_element(By.ID, "page-prev")
        current_url = self.selenium.current_url
        pg_prev.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        pg_begin = self.selenium.find_element(By.ID, "page-begin")
        current_url = self.selenium.current_url
        pg_begin.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))


class TestProductDetailPage(SeleniumWithFirefox):
    def test_tea_detail_page(self):
        tea = TeaFactory.create()

        url = reverse("tea_detail", args=[tea.id])
        self.selenium.get(self.live_server_url + url)
        amount_imput = self.selenium.find_element(By.CSS_SELECTOR, "input[name=amount]")
        total_display = self.selenium.find_element(By.ID, "total")
        initial_total = total_display.text

        move = ActionChains(self.selenium)

        move.click_and_hold(amount_imput).move_by_offset(10, 0).release().perform()
        self.assertNotEqual(initial_total, total_display.text)


class TestHomePage(SeleniumWithFirefox):
    def test_tea_detail_page(self):
        TeaFactory.create_batch(2)

        self.selenium.get(f"{self.live_server_url}/")

        search_input = self.selenium.find_element(By.NAME, "q")
        current_url = self.selenium.current_url

        search_input.send_keys("test tea")
        search_input.send_keys(Keys.RETURN)

        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        products = self.selenium.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(products), 2)
