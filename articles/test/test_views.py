from django.test import TestCase, Client

from articles.models import Article

class TestArticleListView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_article_list_view(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)