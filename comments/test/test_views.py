from django.test import TestCase, Client
from django.contrib.auth.models import User
from catalogue.models import Tea
from comments.models import Comment
from django.urls import reverse

class TestCommentCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        self.product = Tea.objects.create(
            name='test tea 1',
            price = 300.5,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            tea_amount = 300.5
        )

    
    def test_comment_create_view(self):
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))
        
        response = self.client.post('/comments_create/1/', data={'product_id': 1, 'text': 'test comment', 'next_page': '/tea/1/'})
        self.assertEqual(response.status_code, 302)

        self.assertEqual('test comment', Comment.objects.first().text)

    
    def test_comment_reply_view(self):
        comment = Comment.objects.create(
            user = self.user,
            product = self.product,
            text = 'test comment'
        )
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))

        response = self.client.post(f'/comments_create/1/1/', data={
            'product_id': self.product.id, 
            'comment_id': comment.id,
            'text': 'test reply', 
            'next_page': '/tea/1/',
        })
        self.assertEqual(response.status_code, 302)

        self.assertEqual('test reply', Comment.objects.get(parent=comment).text)
