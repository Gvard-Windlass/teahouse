from django.core.management import call_command
from django.test import TestCase
from io import StringIO
from contextlib import redirect_stdout

from articles.models import Article

class TestArticlesLoader(TestCase):
    def test_command_output(self):
        out = StringIO()
        command = 'loadarticles'
        args = ['--csv', 'articles/test/init.csv']
        with out, redirect_stdout(out):
            call_command(command, args, stdout=out)
            expected = 'Created Article Зелёный чай, процесс производства и особенности заварки\nCreated Article Красный чай, процесс производства и особенности заварки\nImport complete'
            self.assertIn(expected, out.getvalue())

    
    def test_image_folder_abs(self):
        out = StringIO()
        command = 'loadarticles'
        args = ['--csv', 'articles/test/init.csv', '--image_folder', 'article_images']
        with out, redirect_stdout(out):
            call_command(command, args)
            image_path = Article.objects.first().thumbnail
            self.assertEqual('article_images/green_tea_article.jpg', image_path)


    def test_image_folder_rel(self):
        out = StringIO()
        command = 'loadarticles'
        args = ['--csv', 'articles/test/init.csv', '--image_folder', 'article_images/']
        with out, redirect_stdout(out):
            call_command(command, args)
            image_path = Article.objects.first().thumbnail
            self.assertEqual('article_images/green_tea_article.jpg', image_path)