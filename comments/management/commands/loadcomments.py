import csv, lorem, datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware

from catalogue.models import Product
from comments.models import Comment


# python manage.py loadcomments --csv comments/management/commands/init.csv --lorem_text True
class Command(BaseCommand):
    help = "Load user and comment data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("--csv", type=str)
        parser.add_argument("--lorem_text", type=bool, default=False)

    def handle(self, *args, **options):
        self.lorem_text = options["lorem_text"]

        try:
            tables = self._load_models(options["csv"])

        except FileNotFoundError:
            raise CommandError(f'File {options["csv"]} does not exist')

        users = self._create_users(tables.get("User", []))
        self._create_comments(tables.get("Comment", []), users)

        print("Import complete")

    def _empty_csv_row(self, row):
        if set(row) == {""}:
            return True
        return False

    def _load_models(self, file_path):
        tables = {}
        header = None
        with open(file_path, encoding="cp1251") as csvfile:
            model_data = csv.reader(csvfile)
            for row in model_data:
                if self._empty_csv_row(row):
                    continue

                if row[0].startswith("Content:"):
                    model_name = row[0].removeprefix("Content:").strip()
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

    def _get_products(self, comments):
        product_names = set([x["product"] for x in comments])
        products = Product.objects.filter(name__in=list(product_names))
        return {x.name: x for x in products}

    def _create_users(self, users):
        db_users = {}

        for user_info in users:
            user, created = User.objects.get_or_create(
                username=user_info["username"],
            )
            if created:
                user.set_password(user_info["password"])
                user.save()
                print(f"Created User {user.username}")

            db_users[user.username] = user
        return db_users

    def _create_comments(self, comments, users):
        db_comments = {}
        products = self._get_products(comments)

        for comment_info in comments:
            text = lorem.sentence() if self.lorem_text else comment_info["text"]

            user = users[comment_info["user"]]
            product = products[comment_info["product"]]
            parent = (
                db_comments[comment_info["parent"]] if comment_info["parent"] else None
            )

            comment, created = Comment.objects.get_or_create(
                timestamp=make_aware(
                    datetime.datetime.strptime(
                        comment_info["timestamp"], "%Y-%m-%d %H:%M:%S"
                    )
                ),
                defaults={
                    "user": user,
                    "product": product,
                    "text": text,
                    "parent": parent,
                },
            )
            if created:
                if not comment.parent:
                    print(
                        f"Created comment by {comment.user.username} for {comment.product.name}"
                    )
                else:
                    print(
                        f"Created reply by {comment.user.username} in {comment.product.name} comments"
                    )

            db_comments[comment_info["timestamp"]] = comment
