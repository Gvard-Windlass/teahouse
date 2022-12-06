from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.views.generic.list import ListView
import json

from .wishlist import Wishlist
from catalogue.models import Product


class WishlistAddView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        product_id = int(json.loads(request.body).get('productid'))
        product = get_object_or_404(Product, pk=product_id)

        wishlist = Wishlist(request)
        wishlist.add(product)

        return JsonResponse({})


class WishlistRemoveView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        product_id = int(json.loads(request.body).get('productid'))
        product = get_object_or_404(Product, pk=product_id)

        wishlist = Wishlist(request)
        wishlist.remove(product)
        
        return JsonResponse({})


class WishlistGetView(View):
    def get(self, request, *args, **kwargs):
        wishlist = Wishlist(request)

        return JsonResponse({'wishlist': wishlist.get_ids()})


class WishlistListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalogue/products.html'

    def get_queryset(self):
        wishlist = Wishlist(self.request)
        return wishlist.get_products()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_title'] = 'Избранное'
        return context