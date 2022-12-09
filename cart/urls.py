from django.urls import path
from . import views

urlpatterns = [
    path('cart_add/', views.AddToCartView.as_view(), name='cart_add'),
    path('cart/', views.CartView.as_view(), name='cart'),
]