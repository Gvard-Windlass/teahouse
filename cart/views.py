from django.views import View
from django.http import HttpRequest
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

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