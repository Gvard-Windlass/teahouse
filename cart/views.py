from django.views import View
from django.http import HttpRequest
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.conf import settings

from .models import Cart


class AddToCartView(LoginRequiredMixin, View):
    login_url = "/login"

    def post(self, request: HttpRequest, *args, **kwargs):
        amount = request.POST.get("amount")
        product_id = int(request.POST.get("productId"))

        Cart.objects.add_to_cart(product_id, request.user, amount)

        nextPage = request.POST.get("nextPage")
        return redirect(nextPage)


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = "/login"

    def post(self, request: HttpRequest, *args, **kwargs):
        product_id = int(request.POST.get("productId"))

        Cart.objects.remove_from_cart(product_id, request.user)

        return redirect("cart")


class CartView(LoginRequiredMixin, ListView):
    model = Cart
    context_object_name = "cart_items"
    template_name = "cart/cart.html"

    def get_queryset(self):
        cart_items = Cart.objects.get_user_cart_content(self.request.user)
        return cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["amount_step"] = settings.AMOUNT_STEP
        context["total"] = Cart.objects.get_cart_total(self.request.user)
        return context
