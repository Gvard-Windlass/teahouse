from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views import View
from .wishlist import Wishlist
from catalogue.models import Product
from django_ajax.mixin import AJAXMixin
import json


class WishlistAddView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        wishlist = Wishlist(request)
        
        product_id = int(json.loads(request.body).get('productid'))
        product = get_object_or_404(Product, pk=product_id)
        
        wishlist.add(product)
        return JsonResponse({})


class WishlistRemoveView(View):
    def post(self, request, *args, **kwargs):
        wishlist = Wishlist(request)
        
        product_id = int(json.loads(request.body).get('productid'))
        product = get_object_or_404(Product, pk=product_id)
        
        wishlist.remove(product)
        return JsonResponse({})


class WishlistGetView(View):
    def get(self, request, *args, **kwargs):
        wishlist = Wishlist(request)

        return JsonResponse({'wishlist': wishlist.get_ids()})