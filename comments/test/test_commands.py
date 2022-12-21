from django.core.management import call_command
from django.test import TestCase
from io import StringIO
from contextlib import redirect_stdout
from catalogue.models import Tea
from comments.models import Comment
from test.factories import TeaFactory


class TestCSVLoader(TestCase):
    def setUp(self) -> None:
        TeaFactory.create(name='Черный чай №1')


    def test_command_output(self):
        out = StringIO()
        command = 'loadcomments'
        args = ['--csv', 'comments/test/init.csv']
        with out, redirect_stdout(out):
            call_command(command, args, stdout=out)
            expected = 'Created User alice\nCreated User bob\nCreated comment by alice for Черный чай №1\nCreated comment by bob for Черный чай №1\nCreated reply by alice in Черный чай №1 comments\nCreated reply by bob in Черный чай №1 comments\nImport complete'
            self.assertIn(expected, out.getvalue())


    def test_text_generation(self):
        out = StringIO()
        command = 'loadcomments'
        args = ['--csv', 'comments/test/init.csv', '--lorem_text', True]
        with out, redirect_stdout(out):
            call_command(command, args)
            description = Comment.objects.first().text
            self.assertNotEqual('', description)