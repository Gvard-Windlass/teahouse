from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from test.factories import ArticleFactory

import test.selenium_setup as setup


class TestArticlesPage(StaticLiveServerTestCase):
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

    def test_articles_page(self):
        ArticleFactory.create_batch(2)

        url = reverse("articles")
        self.selenium.get(self.live_server_url + url)
        articles = self.selenium.find_elements(By.CLASS_NAME, "card")

        self.assertEqual(len(articles), 2)


class TestArticleDetailsPage(StaticLiveServerTestCase):
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

    def test_article_details_page(self):
        article = ArticleFactory.create(body="test body")

        url = reverse("article_detail", args=[article.id])
        self.selenium.get(self.live_server_url + url)

        article_body = self.selenium.find_element(
            By.XPATH, "//*[contains(text(), 'test body')]"
        )
        self.assertEqual(article_body.tag_name, "p")
