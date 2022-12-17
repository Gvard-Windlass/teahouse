from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_catalogue/', views.ProductListView.as_view(), name='products_all'),
    path('product_catalogue/<str:product>/', views.ProductListView.as_view(), name='product_by_section'),
    path('product_catalogue/<str:product>/<str:product_type>/', views.ProductListView.as_view(), name='product_by_type'),
    path('tea/<int:pk>/', views.TeaDetailView.as_view(), name='tea_detail'),
    path('utensil/<int:pk>/', views.UtensilDetailView.as_view(), name='utensil_detail'),
]
