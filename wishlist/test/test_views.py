from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from wishlist.wishlist import Wishlist
from wishlist.views import WishlistAddView, WishlistRemoveView, WishlistGetView
from catalogue.models import Product
import json


class TestWishlistAddView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


    def test_wishlist_add_view(self):
        Product.objects.create(
            name='test product', 
            price = 10.5,
            description = 'product for testing',
            product_type = 'Misc'
        )
        request = self.factory.post(
            '/wishlist_add/', 
            data = {'productid': '1'},
            content_type='application/json'
        )

        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()

        response = WishlistAddView().post(request)
        wishlist = Wishlist(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(1, wishlist.get_ids())


class TestWishlistRemoveView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


    def test_wishlist_add_view(self):
        product = Product.objects.create(
            name='test product', 
            price = 10.5,
            description = 'product for testing',
            product_type = 'Misc'
        )
        request = self.factory.post(
            '/wishlist_remove/', 
            data = {'productid': '1'},
            content_type='application/json'
        )
        
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()

        wishlist = Wishlist(request)
        wishlist.add(product)
        self.assertIn(1, wishlist.get_ids())
        
        response = WishlistRemoveView().post(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(1, wishlist.get_ids())


class TestWishlistGet(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    
    def test_wishlist_get_view(self):
        product = Product.objects.create(
            name='test product', 
            price = 10.5,
            description = 'product for testing',
            product_type = 'Misc'
        )
        request = self.factory.get('/wishlist_get/')

        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()

        wishlist = Wishlist(request)
        wishlist.add(product)
        self.assertIn(1, wishlist.get_ids())

        response = WishlistGetView().get(request)
        response_data = json.loads(response.content)['wishlist']
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(1, response_data)
