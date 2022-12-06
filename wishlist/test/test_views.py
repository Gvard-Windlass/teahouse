from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, AnonymousUser
from wishlist.wishlist import Wishlist
from wishlist.views import WishlistAddView, WishlistRemoveView, WishlistGetView
from catalogue.models import Product
import json


class TestWishlistAddView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_wishlist_add_session(self):
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
        request.user = AnonymousUser()

        response = WishlistAddView().post(request)
        wishlist = Wishlist(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(1, wishlist.get_ids())

    
    def test_wishlist_add_authenticated(self):
        User.objects.create_user(
            username = 'gvard',
            password = 'Bk7^31&3LDXt',
        )
        Product.objects.create(
            name='test product', 
            price = 10.5,
            description = 'product for testing',
            product_type = 'Misc'
        )
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))
        
        response = self.client.post('/wishlist_add/', 
            data = {'productid': '1'},
            content_type='application/json'
        )

        product_id = User.objects.get(id=1).product_set.first().id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, product_id)


class TestWishlistRemoveView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()


    def test_wishlist_remove_session(self):
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
        request.user = AnonymousUser()

        wishlist = Wishlist(request)
        wishlist.add(product)
        self.assertIn(1, wishlist.get_ids())
        
        response = WishlistRemoveView().post(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(1, wishlist.get_ids())


    def test_wishlist_remove_authenticated(self):
        user = User.objects.create_user(
            username = 'gvard',
            password = 'Bk7^31&3LDXt',
        )
        product = Product.objects.create(
            name='test product', 
            price = 10.5,
            description = 'product for testing',
            product_type = 'Misc'
        )
        product.users_wishlist.add(user)
        user.save()
        product.save()

        self.assertTrue(user.product_set.first().id, 1)
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))

        response = self.client.post(
            '/wishlist_remove/', 
            data = {'productid': '1'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(User.objects.get(id=1).product_set.all()))


class TestWishlistGetView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    
    def test_wishlist_get_session(self):
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
        request.user = AnonymousUser()

        wishlist = Wishlist(request)
        wishlist.add(product)
        self.assertIn(1, wishlist.get_ids())

        response = WishlistGetView().get(request)
        response_data = json.loads(response.content)['wishlist']
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(1, response_data)


    def test_wishlist_get_authenticated(self):
        user = User.objects.create_user(
            username = 'gvard',
            password = 'Bk7^31&3LDXt',
        )
        product = Product.objects.create(
            name='test product', 
            price = 10.5,
            description = 'product for testing',
            product_type = 'Misc'
        )
        product.users_wishlist.add(user)
        user.save()
        product.save()

        self.assertTrue(user.product_set.first().id, 1)
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))

        response = self.client.get('/wishlist_get/')
        response_data = json.loads(response.content)['wishlist']
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(1, response_data)


class TestWishlistDisplayView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_wishlist_display_anonymous(self):
        response = self.client.get('/wishlist_display/')
        self.assertEqual(response.status_code, 200)


    def test_wishlist_display_authenticated(self):
        user = User.objects.create_user(
            username = 'gvard',
            password = 'Bk7^31&3LDXt',
        )
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))

        response = self.client.get('/wishlist_display/')
        self.assertEqual(response.status_code, 200)