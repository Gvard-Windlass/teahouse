from django.urls import path
import django.contrib.auth.views as auth_views
from . import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="catalogue/home.html", next_page="home"
        ),
        name="logout",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="account/login.html", next_page="home"
        ),
        name="login",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "profile/password/",
        auth_views.PasswordChangeView.as_view(
            template_name="account/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "profile/password_change_done",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="account/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset.html",
            subject_template_name="account/password_reset_subject.txt",
            email_template_name="account/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
