from django.test import TestCase, Client
from django.urls import reverse
from catalogue.models import Tea
from test.factories import TeaFactory, UtensilFactory

class TestTeaListView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_tea_list_view_specific(self):
        url = reverse('product_by_type', args=['Tea', 'Black'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_tea_list_view_all(self):
        url = reverse('product_by_section', args=['Tea'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestUtensilListView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_utensil_list_view_specific(self):
        url = reverse('product_by_type', args=['Utensil', 'Cup'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_utensil_list_view_all(self):
        url = reverse('product_by_section', args=['Utensil'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestTeaDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_tea_exist_detail_view(self):
        TeaFactory.create()
        url = reverse('tea_detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_tea_not_exist_detail_view(self):
        url = reverse('tea_detail', args=[2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestUtensilDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_utensil_exist_detail_view(self):
        UtensilFactory.create()
        url = reverse('utensil_detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_utensil_not_exist_detail_view(self):
        url = reverse('utensil_detail', args=[2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestProductSearchView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_product_search_view(self):
        url = reverse('product_search')
        response = self.client.get(url, data={'q': 'tea'})
        self.assertEqual(response.status_code, 200)