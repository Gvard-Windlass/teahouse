from django.test import TestCase, Client

from cart.models import Cart
from test.factories import TeaFactory, UserFactory


class TestCartManager(TestCase):
    def setUp(self):
        self.client = Client()

        product = TeaFactory.create()
        TeaFactory.create()

        self.user = UserFactory.create()
        Cart.objects.create(product=product, user=self.user, amount=200)

    def test_add_new_to_cart(self):
        Cart.objects.add_to_cart(2, self.user, 100)
        cart = self.user.cart_set.all()
        self.assertEqual(len(cart), 2)

    def test_add_existent_to_cart(self):
        Cart.objects.add_to_cart(1, self.user, 100)
        cart_item = Cart.objects.first()
        self.assertEqual(cart_item.amount, 100)

        Cart.objects.add_to_cart(1, self.user, 200, True)
        cart_item = Cart.objects.first()
        self.assertEqual(cart_item.amount, 300)

    def test_remove_from_cart(self):
        Cart.objects.remove_from_cart(1, self.user)
        cart = Cart.objects.all()
        self.assertEqual(len(cart), 0)
