from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tea_catalogue/', views.TeaListView.as_view(), name='tea_all'),
    path('tea_catalogue/<tea_type>/', views.TeaListView.as_view(), name='tea_by_type'),
    path('tea/<int:pk>/', views.TeaDetailView.as_view(), name='tea_detail'),
]
