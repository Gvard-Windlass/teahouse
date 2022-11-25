from django.core.management import call_command
from django.test import TestCase
from io import StringIO
from contextlib import redirect_stdout
from catalogue.models import Tea

class TestCSVLoader(TestCase):
    def test_command_output(self):
        out = StringIO()
        command = 'loadcsv'
        args = ['--csv', 'catalogue/test/init.csv']
        with out, redirect_stdout(out):
            call_command(command, args, stdout=out)
            expected = 'Created Tea Черный чай №1\nCreated Tea Черный чай №2\nCreated Utensil Чашка №1\nCreated Utensil Чашка №2\nImport complete'
            self.assertIn(expected, out.getvalue())


    def test_image_folder_abs(self):
        out = StringIO()
        command = 'loadcsv'
        args = ['--csv', 'catalogue/test/init.csv', '--image_folder', 'product_images']
        with out, redirect_stdout(out):
            call_command(command, args)
            image_path = Tea.objects.get(pk=1).image
            self.assertEqual('product_images/black1.jpg', image_path)


    def test_image_folder_rel(self):
        out = StringIO()
        command = 'loadcsv'
        args = ['--csv', 'catalogue/test/init.csv', '--image_folder', 'product_images/']
        with out, redirect_stdout(out):
            call_command(command, args)
            image_path = Tea.objects.get(pk=1).image
            self.assertEqual('product_images/black1.jpg', image_path)

    
    def test_description_generation(self):
        out = StringIO()
        command = 'loadcsv'
        args = ['--csv', 'catalogue/test/init.csv', '--lorem_description', True]
        with out, redirect_stdout(out):
            call_command(command, args)
            description = Tea.objects.get(pk=1).description
            self.assertNotEqual('', description)