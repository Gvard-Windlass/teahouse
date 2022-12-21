from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from articles.models import Article

import test.selenium_setup as setup

class TestArticlesPage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH), executable_path=setup.DRIVER_PATH)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_articles_page(self):
        Article.objects.create(
            author = 'alice',
            title = 'test article 1',
            summary = 'test summary 1',
            body = 'test body 1'
        )
        Article.objects.create(
            author = 'bob',
            title = 'test article 2',
            summary = 'test summary 2',
            body = 'test body 2'
        )

        self.selenium.get(f'{self.live_server_url}/articles/')
        articles = self.selenium.find_elements(By.CLASS_NAME, 'card')

        self.assertEqual(len(articles), 2)


class TestArticleDetailsPage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH), executable_path=setup.DRIVER_PATH)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_article_details_page(self):
        article = Article.objects.create(
            author = 'alice',
            title = 'test article',
            summary = 'test summary',
            body = 'test body'
        )

        self.selenium.get(f'{self.live_server_url}/articles/{article.id}/')
        
        article_body = self.selenium.find_element(By.XPATH, "//*[contains(text(), 'test body')]")
        self.assertEqual(article_body.tag_name, 'p')
