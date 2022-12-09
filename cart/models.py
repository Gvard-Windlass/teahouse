from django.db import models
from django.contrib.auth.models import User

from catalogue.models import Product


class CartManager(models.Manager):
    def add_to_cart(self, product_id: int, user: User, amount: int, incremental=False):
        product = Product.objects.get(pk=product_id)
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


    def get_user_cart_content(self, user: User):
        return user.cart_set.all()


    def get_user_cart_ids(self, user: User):
        return user.cart_set.all().values_list('product', flat=True)


    def get_cart_item(self, user: User, product: Product):
        cart_item = user.cart_set.filter(product=product)
        if cart_item:
            return cart_item[0]


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    objects = CartManager()