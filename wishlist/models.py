from django.db import models
from django.contrib.auth.models import User

from catalogue.models import Product


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product} in wishlist of {self.user}'