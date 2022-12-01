from django.urls import path
import django.contrib.auth.views as auth_views
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='account/login.html',
        next_page='home'
    ), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/password/', auth_views.PasswordChangeView.as_view(
        template_name='account/password_change.html'
    ), name='password_change'),
    path('profile/password_change_done.html', auth_views.PasswordChangeDoneView.as_view(
        template_name='account/password_change_done.html'
    ), name='password_change_done')
]