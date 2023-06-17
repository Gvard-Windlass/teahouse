from django.urls import reverse
from selenium.webdriver.common.by import By

from test.factories import ArticleFactory

from test.selenium_setup import SeleniumWithFirefox


class TestArticlesPage(SeleniumWithFirefox):
    def test_articles_page(self):
        ArticleFactory.create_batch(2)

        url = reverse("articles")
        self.selenium.get(self.live_server_url + url)
        articles = self.selenium.find_elements(By.CLASS_NAME, "card")

        self.assertEqual(len(articles), 2)


class TestArticleDetailsPage(SeleniumWithFirefox):
    def test_article_details_page(self):
        article = ArticleFactory.create(body="test body")

        url = reverse("article_detail", args=[article.id])
        self.selenium.get(self.live_server_url + url)

        article_body = self.selenium.find_element(
            By.XPATH, "//*[contains(text(), 'test body')]"
        )
        self.assertEqual(article_body.tag_name, "p")
