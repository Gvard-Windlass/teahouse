from django.test import TestCase

from comments.forms import CommentForm
from comments.models import Comment
from test.factories import ProductFactory, UserFactory


class TestCommentForm(TestCase):
    def test_add_comment(self):
        user = UserFactory.create()
        product = ProductFactory.create()
        form_data = {"text": "test comment", "product": product, "next_page": "/tea/1/"}

        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

        comment = form.save(commit=False)
        comment.product = product
        comment.user = user
        comment.save()

        comment = Comment.objects.first()
        self.assertEqual(comment.text, "test comment")
