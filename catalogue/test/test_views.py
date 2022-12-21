from django.test import TestCase, Client
from catalogue.models import Tea
from test.factories import TeaFactory

class TestTeaListView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_tea_list_view_specific(self):
        response = self.client.get('/product_catalogue/Black/')
        self.assertEqual(response.status_code, 200)


    def test_tea_list_view_all(self):
        response = self.client.get('/product_catalogue/')
        self.assertEqual(response.status_code, 200)


class TestTeaDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_tea_detail_view(self):
        TeaFactory.create()

        response = self.client.get('/tea/1/')
        self.assertEqual(response.status_code, 200)


class TestProductSearchView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_tea_detail_view(self):
        response = self.client.get('/product_search/?q=tea')
        self.assertEqual(response.status_code, 200)