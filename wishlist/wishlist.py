from decimal import Decimal
from catalogue.models import Product
from django.http import HttpRequest
from django.conf import settings


class Wishlist:
    def __init__(self, request: HttpRequest):
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.wishlist = wishlist
        self.user = request.user

    
    def add(self, product):
        if self.user.is_authenticated:
            product.users_wishlist.add(self.user)
        else:
            product_id = str(product.id)
            if product_id not in self.wishlist:
                self.wishlist[product_id] = {'price': str(product.price)}
            self.save()


    def remove(self, product):
        if self.user.is_authenticated:
            product.users_wishlist.remove(self.user)
        else:
            product_id = str(product.id)
            if product_id in self.wishlist:
                self.wishlist.pop(product_id)
            self.save()

    
    def save(self):
        self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
        self.session.modified = True


    def get_ids(self):
        if self.user.is_authenticated:
            return list(self.user.product_set.all().values_list('id', flat=True))
        else:
            return [int(x) for x in self.wishlist.keys()]
