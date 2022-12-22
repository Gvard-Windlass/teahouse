from django.test import TestCase, Client

from test.factories import ArticleFactory

class TestArticleListView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_article_list_view(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)


class TestArticleDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_article_exist_detail(self):
        ArticleFactory.create()
        response = self.client.get('/articles/1/')
        self.assertEqual(response.status_code, 200)

    
    def test_article_not_exist_detail(self):
        response = self.client.get('/articles/2/')
        self.assertEqual(response.status_code, 404)