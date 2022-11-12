from django.test import TestCase

from store.models import *

class TestProductModel(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            name='test product', 
            price = 10.5,
            description = 'product for testing',
            product_type = 'Misc'
        )
        self.assertIsInstance(product, Product)


class TestTeaModel(TestCase):
    def test_create_tea(self):
        tea = Tea.objects.create(
            name='test tea',
            price = 300.5,
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            tea_amount = 300.5
        )
        self.assertIsInstance(tea, Tea)