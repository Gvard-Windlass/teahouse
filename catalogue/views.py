from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, TemplateResponseMixin
from django.shortcuts import render
from django.conf import settings

from articles.models import Article
from .models import Product, Tea, Utensil
from cart.models import Cart
from comments.models import Comment
from comments.forms import CommentForm


class HomeView(TemplateView):
    template_name = 'catalogue/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all().order_by('-id')[:3]
        context['products'] = Product.objects.all().order_by('-id')[:10]
        return context


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalogue/products.html'
    paginate_by = 10

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


class ProductSearchView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalogue/products.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        # seems like sqlite are case-sensetive even with icontains for ru
        # https://docs.djangoproject.com/en/4.1/ref/databases/#substring-matching-and-case-sensitivity
        products = Product.objects.filter(name__icontains=query)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_title'] = 'Search results'
        context['query'] = self.request.GET.get('q')
        return context


class ProductContextMixin(TemplateResponseMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['amount_step'] = 1
        context['comment_form'] = CommentForm()
        context['comment_form'].fields['next_page'].initial = self.request.path
        context['comments'] = Comment.objects.filter(product=context['object'].id)
        
        cart_amount = Cart.objects.get_cart_amount(self.request.user, context['object'].id)
        
        product_amount = getattr(context['object'], 'amount', None)

        if cart_amount:
            context['added_to_cart'] = True
            if product_amount:
                if cart_amount <= product_amount:
                    context['initial_value'] = cart_amount
                else:
                    context['initial_value'] = product_amount
        else:
            context['initial_value'] = 1

        return context, cart_amount


class TeaDetailView(ProductContextMixin, DetailView):
    model = Tea
    template_name = 'catalogue/tea_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context, cart_amount = super().get_context_data(**kwargs)
        context['amount_step'] = settings.AMOUNT_STEP

        if not cart_amount:
            context['initial_value'] = settings.AMOUNT_STEP
        
        return context


class UtensilDetailView(ProductContextMixin, DetailView):
    model = Utensil
    tempalte_name = 'catalogue/utensil_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context, cart_amount = super().get_context_data(**kwargs)
        return context