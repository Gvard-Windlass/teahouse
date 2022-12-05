from django.urls import path
import django.contrib.auth.views as auth_views
from . import views

urlpatterns = [
    path('wishlist_get/', views.WishlistGetView.as_view(), name='wishlist_get'),
    path('wishlist_add/', views.WishlistAddView.as_view(), name='wishlist_add'),
    path('wishlist_remove/', views.WishlistRemoveView.as_view(), name='wishlist_remove')
]