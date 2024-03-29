from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from cart.models import Cart
from test.factories import TeaFactory, UserFactory


class TestCartAddView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cart_add_view(self):
        UserFactory.create()
        TeaFactory.create()
        form_data = {"amount": 10, "productId": 1, "nextPage": "/tea/1/"}
        self.assertTrue(self.client.login(username="gvard", password="Bk7^31&3LDXt"))

        url = reverse("cart_add")
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(1, User.objects.first().cart_set.first().id)


class TestCartView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cart_view(self):
        UserFactory.create()
        self.assertTrue(self.client.login(username="gvard", password="Bk7^31&3LDXt"))

        url = reverse("cart")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCartRemoveView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cart_remove(self):
        user = UserFactory.create()
        product = TeaFactory.create()
        Cart.objects.create(product=product, user=user, amount=200)

        self.assertTrue(self.client.login(username="gvard", password="Bk7^31&3LDXt"))

        url = reverse("cart_remove")
        response = self.client.post(url, data={"productId": 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Cart.objects.all()), 0)
