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