from django.test import TestCase

from articles.models import *
from test.factories import ArticleFactory


class TestArticleModel(TestCase):
    def test_create_article(self):
        article = ArticleFactory.create()
        self.assertIsInstance(article, Article)
