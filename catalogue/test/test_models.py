from django.test import TestCase

from catalogue.models import *
from test.factories import ProductFactory, TeaFactory, UtensilFactory

class TestProductModel(TestCase):
    def test_create_product(self):
        product = ProductFactory.create()
        self.assertIsInstance(product, Product)


class TestTeaModel(TestCase):
    def test_create_tea(self):
        tea = TeaFactory.create()
        self.assertIsInstance(tea, Tea)


class TestUtensilModel(TestCase):
    def test_create_utensil(self):
        utensil = UtensilFactory.create()
        self.assertIsInstance(utensil, Utensil)