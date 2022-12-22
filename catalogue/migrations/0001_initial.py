# Generated by Django 4.1.1 on 2022-12-22 12:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('Tea', 'Tea'), ('Utensil', 'Utensil'), ('Misc', 'Miscellaneous')], max_length=20)),
                ('name', models.CharField(max_length=70)),
                ('price', models.FloatField()),
                ('amount', models.PositiveIntegerField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('description', models.TextField()),
                ('tea_type', models.CharField(choices=[('Black', 'Black'), ('Dark', 'Dark'), ('Green', 'Green'), ('Oolong', 'Oolong'), ('Puer', 'Puer'), ('White', 'White'), ('Yellow', 'Yellow')], max_length=20, null=True)),
                ('tea_year', models.PositiveSmallIntegerField(null=True)),
                ('utensil_type', models.CharField(choices=[('Cup', 'Cup'), ('Kettle', 'Kettle'), ('Teapot', 'Teapot'), ('Tureen', 'Tureen')], max_length=20, null=True)),
                ('utensil_material', models.CharField(choices=[('Ceramic', 'Ceramic'), ('Metal', 'Metal'), ('Clay', 'Clay'), ('Porcelain', 'Porcelain')], max_length=20, null=True)),
                ('users_cart', models.ManyToManyField(blank=True, through='cart.Cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
