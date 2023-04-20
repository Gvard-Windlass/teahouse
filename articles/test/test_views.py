from django.test import TestCase, Client
from django.urls import reverse

from test.factories import ArticleFactory


class TestArticleListView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_article_list_view(self):
        url = reverse("articles")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestArticleDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_article_exist_detail(self):
        ArticleFactory.create()
        url = reverse("article_detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_not_exist_detail(self):
        url = reverse("article_detail", args=[2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
