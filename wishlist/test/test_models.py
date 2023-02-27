from django.test import TestCase

from wishlist.models import *
from test.factories import ProductFactory, UserFactory


class TestWishlistModel(TestCase):
    def test_create_wishlist_item(self):
        product = ProductFactory.create()
        user = UserFactory.create()
        wishlist = Wishlist.objects.create(product=product, user=user)
        self.assertIsInstance(wishlist, Wishlist)
