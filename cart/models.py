from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.conf import settings

from catalogue.models import Product


class CartManager(models.Manager):
    def add_to_cart(self, product_id: int, user: User, amount: int, incremental=False):
        product = get_object_or_404(Product, pk=product_id)
        current_cart = self.get_user_cart_ids(user)
        
        if product.id in current_cart:
            cart_item = self.get_cart_item(user, product)
            if incremental:
                cart_item.amount += amount
            else:
                cart_item.amount = amount
            cart_item.save()
        else:
            Cart.objects.create(product=product, user=user, amount=amount)


    def remove_from_cart(self, product_id: int, user: User):
        product = get_object_or_404(Product, pk=product_id)
        cart_item = self.get_cart_item(user, product)
        if cart_item:
            cart_item.delete()


    def get_user_cart_content(self, user: User):
        return user.cart_set.all()


    def get_user_cart_ids(self, user: User):
        return user.cart_set.all().values_list('product', flat=True)


    def get_cart_item(self, user: User, product: Product):
        cart_item = user.cart_set.filter(product=product)
        if cart_item:
            return cart_item[0]


    def get_cart_amount(self, user: User, product_id: int):
        try:
            cart_item = user.cart_set.get(product__id=product_id)
            return cart_item.amount
        except:
            return

    
    def get_cart_total(self, user: User):
        total = 0
        for cart_item in user.cart_set.all():
            if cart_item.product.product_type == 'Tea':
                total += cart_item.amount*cart_item.product.price/settings.AMOUNT_STEP
            else:
                total += cart_item.amount*cart_item.product.price
        return total


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    objects = CartManager()

    def __str__(self):
        return f'{self.amount} of {self.product} by {self.user}'