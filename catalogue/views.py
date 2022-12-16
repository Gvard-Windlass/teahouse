from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.conf import settings

from .models import Product, Tea, Utensil
from cart.models import Cart
from comments.models import Comment
from comments.forms import CommentForm


def home(request):
    return render(request, 'catalogue/home.html')


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalogue/products.html'


    def get_queryset(self):
        product_section = self.kwargs.get('product')
        product_type = self.kwargs.get('product_type')
        return Product.objects.filter_products(product_section, product_type)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        product_section = self.kwargs.get('product')
        product_type = self.kwargs.get('product_type')
        context['products_title'] = Product.objects.get_product_title(product_section, product_type)
        
        return context


class TeaDetailView(DetailView):
    model = Tea
    template_name = 'catalogue/tea_detail.html'
    context_object_name = 'tea'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['amount_step'] = settings.AMOUNT_STEP
        context['comment_form'] = CommentForm()
        context['comment_form'].fields['next_page'].initial = self.request.path
        context['comments'] = Comment.objects.filter(product=context['object'].id)

        cart_amount = Cart.objects.get_cart_amount(self.request.user, context['object'].id)
        if cart_amount:
            context['added_to_cart'] = True
            if cart_amount <= context['object'].tea_amount:
                context['initial_value'] = cart_amount
            else:
                context['initial_value'] = context['object'].tea_amount
        else:
            context['initial_value'] = settings.AMOUNT_STEP
        
        return context