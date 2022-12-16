import csv, lorem

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from articles.models import Article

# python manage.py loadarticles --csv articles/management/commands/init.csv --image_folder article_images
class Command(BaseCommand):
    help = 'Load article data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str)
        parser.add_argument('--image_folder', type=str, default='')

    
    def handle(self, *args, **options):
        self.image_folder = options['image_folder']

        if self.image_folder and not self.image_folder.endswith('/'):
            self.image_folder += '/'

        try:
            tables = self._load_models(options['csv'])

        except FileNotFoundError:
            raise CommandError(f'File {options["csv"]} does not exist')

        self._create_articles(tables.get('Article', []))

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


    def _create_articles(self, articles):
        for article_info in articles:
            article, created = Article.objects.get_or_create(
                title = article_info['title'],
                defaults={
                    'author': article_info['author'],
                    'thumbnail': self.image_folder+article_info['thumbnail'],
                    'summary': article_info['summary'],
                    'body': article_info['body']
                }
            )
            if created:
                print(f'Created Article {article.title}')
