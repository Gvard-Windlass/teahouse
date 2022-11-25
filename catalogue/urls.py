from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tea/', views.TeaListView.as_view(), name='tea_all'),
    path('tea/<tea_type>/', views.TeaListView.as_view(), name='tea_by_type'),
]
