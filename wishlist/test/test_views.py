from django.test import TestCase, Client
from django.urls import reverse
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, AnonymousUser
from wishlist.wishlist import WishlistService
from wishlist.views import WishlistAddView, WishlistRemoveView, WishlistGetView
from test.factories import ProductFactory, UserFactory
import json


class TestWishlistAddView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.url = reverse("wishlist_add")

    def test_wishlist_add_session(self):
        ProductFactory.create()

        request = self.factory.post(
            self.url, data={"productid": "1"}, content_type="application/json"
        )

        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        request.user = AnonymousUser()

        response = WishlistAddView().post(request)
        wishlist = WishlistService(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(1, wishlist.get_ids())

    def test_wishlist_add_authenticated(self):
        UserFactory.create()
        ProductFactory.create()
        self.assertTrue(self.client.login(username="gvard", password="Bk7^31&3LDXt"))

        response = self.client.post(
            self.url, data={"productid": "1"}, content_type="application/json"
        )

        product_id = User.objects.get(id=1).users_wishlist.first().id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, product_id)


class TestWishlistRemoveView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.url = reverse("wishlist_remove")

    def test_wishlist_remove_session(self):
        product = ProductFactory.create()

        request = self.factory.post(
            self.url, data={"productid": "1"}, content_type="application/json"
        )

        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        request.user = AnonymousUser()

        wishlist = WishlistService(request)
        wishlist.add(product)
        self.assertIn(1, wishlist.get_ids())

        response = WishlistRemoveView().post(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(1, wishlist.get_ids())

    def test_wishlist_remove_authenticated(self):
        user = UserFactory.create()
        product = ProductFactory.create()

        product.users_wishlist.add(user)
        user.save()
        product.save()

        self.assertTrue(user.users_wishlist.first().id, 1)
        self.assertTrue(self.client.login(username="gvard", password="Bk7^31&3LDXt"))

        response = self.client.post(
            self.url, data={"productid": "1"}, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(User.objects.get(id=1).users_wishlist.all()))


class TestWishlistGetView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.url = reverse("wishlist_get")

    def test_wishlist_get_session(self):
        product = ProductFactory.create()
        request = self.factory.get(self.url)

        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        request.user = AnonymousUser()

        wishlist = WishlistService(request)
        wishlist.add(product)
        self.assertIn(1, wishlist.get_ids())

        response = WishlistGetView().get(request)
        response_data = json.loads(response.content)["wishlist"]

        self.assertEqual(response.status_code, 200)
        self.assertIn(1, response_data)

    def test_wishlist_get_authenticated(self):
        user = UserFactory.create()
        product = ProductFactory.create()
        product.users_wishlist.add(user)
        user.save()
        product.save()

        self.assertTrue(user.users_wishlist.first().id, 1)
        self.assertTrue(self.client.login(username="gvard", password="Bk7^31&3LDXt"))

        response = self.client.get(self.url)
        response_data = json.loads(response.content)["wishlist"]

        self.assertEqual(response.status_code, 200)
        self.assertIn(1, response_data)


class TestWishlistDisplayView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("wishlist_display")

    def test_wishlist_display_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_wishlist_display_authenticated(self):
        UserFactory.create()
        self.assertTrue(self.client.login(username="gvard", password="Bk7^31&3LDXt"))

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
