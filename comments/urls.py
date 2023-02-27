from django.urls import path
from . import views

urlpatterns = [
    path(
        "comments_create/<int:product_id>/",
        views.CommentsCreateView.as_view(),
        name="comments_create",
    ),
    path(
        "comments_create/<int:product_id>/<int:comment_id>/",
        views.CommentsCreateView.as_view(),
        name="comments_create",
    ),
]
