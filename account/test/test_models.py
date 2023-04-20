from django.contrib.auth.models import User
from django.test import TestCase

from account.models import *


class TestCustomerModel(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="test user",
            password="test password",
        )
        user.customer.birthday = "2000-01-01"
        user.save()

    def test_create_customer(self):
        user = User.objects.get(username="test user")
        self.assertIsInstance(user.customer, Customer)
        self.assertEqual(str(user.customer.birthday), "2000-01-01")
