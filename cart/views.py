from django.views import View
from django.http import HttpRequest
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from .models import Cart
from catalogue.models import Product

class AddToCartView(LoginRequiredMixin, View):
    login_url = '/login'

    def post(self, request: HttpRequest, *args, **kwargs):
        amount = request.POST.get('amount')
        tea_id = int(request.POST.get('teaId'))
        
        product = Product.objects.get(pk=tea_id)
        Cart.objects.create(product=product, user=request.user, amount=amount)

        nextPage = request.POST.get('nextPage')
        return redirect(nextPage)


class CartView(LoginRequiredMixin, ListView):
    model = Cart
    context_object_name = 'cart_items'
    template_name = 'cart/cart.html'

    def get_queryset(self):
        cart_items = self.request.user.cart_set.all()
        return cart_items