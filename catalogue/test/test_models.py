from django.test import TestCase

from catalogue.models import *
from test.factories import TeaFactory

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
        tea = TeaFactory.create()
        self.assertIsInstance(tea, Tea)


class TestUtensilModel(TestCase):
    def test_create_utensil(self):
        tea = Utensil.objects.create(
            name='test cup',
            price = 100.5,
            amount = 10,
            description = 'utensil for testing',
            product_type = 'Utensil',
            utensil_type = 'Cup',
            utensil_material = 'Ceramic',
        )
        self.assertIsInstance(tea, Utensil)