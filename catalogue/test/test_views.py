from django.test import TestCase, Client
from catalogue.models import Tea
from test.factories import TeaFactory, UtensilFactory

class TestTeaListView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_tea_list_view_specific(self):
        response = self.client.get('/product_catalogue/Tea/Black/')
        self.assertEqual(response.status_code, 200)


    def test_tea_list_view_all(self):
        response = self.client.get('/product_catalogue/Tea/')
        self.assertEqual(response.status_code, 200)


class TestUtensilListView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_utensil_list_view_specific(self):
        response = self.client.get('/product_catalogue/Utensil/Cup/')
        self.assertEqual(response.status_code, 200)


    def test_utensil_list_view_all(self):
        response = self.client.get('/product_catalogue/Utensil/')
        self.assertEqual(response.status_code, 200)


class TestTeaDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_tea_exist_detail_view(self):
        TeaFactory.create()
        response = self.client.get('/tea/1/')
        self.assertEqual(response.status_code, 200)

    
    def test_tea_not_exist_detail_view(self):
        response = self.client.get('/tea/2/')
        self.assertEqual(response.status_code, 404)


class TestUtensilDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_utensil_exist_detail_view(self):
        UtensilFactory.create()
        response = self.client.get('/utensil/1/')
        self.assertEqual(response.status_code, 200)

    
    def test_utensil_not_exist_detail_view(self):
        response = self.client.get('/utensil/2/')
        self.assertEqual(response.status_code, 404)


class TestProductSearchView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_product_search_view(self):
        response = self.client.get('/product_search/?q=tea')
        self.assertEqual(response.status_code, 200)