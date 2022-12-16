from django.test import TestCase
from django.contrib.auth.models import User

from comments.forms import CommentForm
from comments.models import Comment
from catalogue.models import Product

class TestCommentForm(TestCase):
    def test_add_comment(self):
        user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        product = Product.objects.create(
            name='test product', 
            price = 10.5,
            description = 'product for testing',
            product_type = 'Misc'
        )
        form_data = {
            'text': 'test comment',
            'product': product,
            'next_page': '/tea/1/'
        }

        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        comment = form.save(commit=False)
        comment.product = product
        comment.user = user
        comment.save()
        
        comment = Comment.objects.first()
        self.assertEqual(comment.text, 'test comment')