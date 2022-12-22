from django.test import TestCase

from comments.models import *
from test.factories import ProductFactory, UserFactory

class TestCommentModel(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product = ProductFactory.create()

    def test_create_comment(self):
        comment = Comment.objects.create(
            user = self.user,
            product = self.product,
            text = 'test comment'
        )
        self.assertIsInstance(comment, Comment)

    
    def test_create_reply(self):
        comment = Comment.objects.create(
            user = self.user,
            product = self.product,
            text = 'test comment'
        )
        reply = Comment.objects.create(
            user = self.user,
            product = self.product,
            text = 'test reply',
            parent = comment
        )
        self.assertIsInstance(reply, Comment)