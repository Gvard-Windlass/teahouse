from django.test import TestCase, Client
from catalogue.models import Tea


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
        Tea.objects.create(
            name='test tea 1',
            price = 300.5,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            tea_amount = 300.5
        )

        response = self.client.get('/tea/1/')
        self.assertEqual(response.status_code, 200)