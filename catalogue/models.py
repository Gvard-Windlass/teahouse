from django.db import models
from django.contrib.auth.models import User


class ProductManager(models.Manager):
    # TODO - need better names
    def filter_products(self, product_section, product_type):
        if product_section:
            if product_type:
                product_filters = {
                    'product_type': product_section,
                    f'{product_section.lower()}_type': product_type
                }
                return Product.objects.filter(**product_filters)
            return Product.objects.filter(product_type=product_section)
        return Product.objects.all()

    
    def get_product_title(self, product_section, product_type):
        if product_section:
            if product_type:
                if product_section == 'Tea':
                    return f'{product_type} {product_section}'
                
                return f'{product_type}s'
            
            return f'All {product_section}s'
        return 'All Products'


class Product(models.Model):
    class ProductType(models.TextChoices):
        Tea = 'Tea', 'Tea'
        Utensil = 'Utensil', 'Utensil'
        Misc = 'Misc', 'Miscellaneous'

    product_type = models.CharField(choices=ProductType.choices, max_length=20)

    # common fields
    name = models.CharField(max_length=70)
    price = models.FloatField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    description = models.TextField()
    users_wishlist = models.ManyToManyField(User, blank=True, related_name='wishlist')
    users_cart = models.ManyToManyField(User, blank=True, through='cart.Cart')
    objects = ProductManager()

    # tea fields
    class TeaType(models.TextChoices):
        Black = 'Black', 'Black'
        Dark = 'Dark', 'Dark'
        Green = 'Green', 'Green'
        Oolong = 'Oolong', 'Oolong'
        Puer = 'Puer', 'Puer'
        White = 'White', 'White'
        Yellow = 'Yellow', 'Yellow'

    tea_type = models.CharField(choices=TeaType.choices, max_length=20, null=True)
    tea_year = models.PositiveSmallIntegerField(null=True)
    tea_amount = models.FloatField(null=True)

    # utensil fields
    class UtensilType(models.TextChoices):
        Cup = 'Cup', 'Cup'
        Kettle = 'Kettle', 'Kettle'
        Teapot = 'Teapot', 'Teapot'
        Tureen = 'Tureen', 'Tureen'

    class UtensilMaterial(models.TextChoices):
        Ceramic = 'Ceramic', 'Ceramic'
        Metal = 'Metal', 'Metal'
        Clay = 'Clay', 'Clay'
        Porcelain = 'Porcelain', 'Porcelain'

    utensil_type = models.CharField(choices=UtensilType.choices, max_length=20, null=True)
    utensil_material = models.CharField(choices = UtensilMaterial.choices, max_length=20, null=True)
    utensil_amount = models.PositiveIntegerField(null=True)


class TeaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_type='Tea')

class Tea(Product):
    objects = TeaManager()

    class Meta:
        proxy = True


class UtensilManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_type='Utensil')

class Utensil(Product):
    objects = UtensilManager()

    class Meta:
        proxy = True