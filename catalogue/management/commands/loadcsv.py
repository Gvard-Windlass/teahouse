import csv, lorem

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from catalogue.models import Product, Tea, Utensil

# python manage.py loadcsv --csv catalogue/management/commands/init.csv --image_folder product_images --lorem_description True
class Command(BaseCommand):
    help = 'Load product data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str)
        parser.add_argument('--image_folder', type=str, default='')
        parser.add_argument('--lorem_description', type=bool, default=False)

    
    def handle(self, *args, **options):
        self.image_folder = options['image_folder']
        self.lorem_description = options['lorem_description']

        if self.image_folder and not self.image_folder.endswith('/'):
            self.image_folder += '/'

        try:
            tables = self._load_models(options['csv'])

        except FileNotFoundError:
            raise CommandError(f'File {options["csv"]} does not exist')

        self._create_tea_products(tables.get('Tea', []))
        self._create_utensil_products(tables.get('Utensil', []))

        print('Import complete')


    def _empty_csv_row(self, row):
        if set(row) == {''}:
            return True
        return False


    def _load_models(self, file_path):
        tables = {}
        header = None
        with open(file_path) as csvfile:
            model_data = csv.reader(csvfile)
            for row in model_data:
                if self._empty_csv_row(row):
                    continue
                
                if row[0].startswith('Content:'):
                    model_name = row[0].removeprefix('Content:').strip()
                    tables[model_name] = list()
                    header = None
                    continue

                if header is None:
                    header = row
                    continue
                
                item_dict = dict(zip(header, row))
                tables[model_name].append(item_dict)
        csvfile.close()
        return tables


    def _create_tea_products(self, products):
        for tea_info in products:
            description = lorem.text() if self.lorem_description \
                else tea_info['description']

            tea, created = Tea.objects.get_or_create(
                name = tea_info['name'],
                defaults={
                    'product_type': tea_info['product_type'],
                    'price': tea_info['price'],
                    'image': self.image_folder+tea_info['image'],
                    'description': description,
                    'tea_type': tea_info['tea_type'],
                    'tea_year': tea_info['tea_year'],
                    'tea_amount': tea_info['tea_amount'],
                }
            )
            if created:
                print(f'Created Tea {tea.name}')


    def _create_utensil_products(self, products):
        for utensil_info in products:
            description = lorem.text() if self.lorem_description \
                else utensil_info['description']

            utensil, created = Utensil.objects.get_or_create(
                name = utensil_info['name'],
                defaults={
                    'product_type': utensil_info['product_type'],
                    'price': utensil_info['price'],
                    'image': self.image_folder+utensil_info['image'],
                    'description': description,
                    'utensil_type': utensil_info['utensil_type'],
                    'utensil_material': utensil_info['utensil_material'],
                    'utensil_amount': utensil_info['utensil_amount'],
                }
            )
            if created:
                print(f'Created Utensil {utensil.name}')
