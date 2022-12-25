# Generated by Django 4.1.1 on 2022-12-22 12:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='users_wishlist',
            field=models.ManyToManyField(blank=True, related_name='users_wishlist', through='wishlist.Wishlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Tea',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('catalogue.product',),
        ),
        migrations.CreateModel(
            name='Utensil',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('catalogue.product',),
        ),
    ]