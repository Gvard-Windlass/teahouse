from django.test import TestCase

from cart.models import *
from test.factories import ProductFactory, UserFactory


class TestCartModel(TestCase):
    def test_create_cart_item(self):
        product = ProductFactory.create()
        user = UserFactory.create()
        cart = Cart.objects.create(product=product, user=user, amount=10)
        self.assertIsInstance(cart, Cart)
