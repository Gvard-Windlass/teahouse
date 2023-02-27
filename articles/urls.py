from django.urls import path
from . import views

urlpatterns = [
    path("articles/", views.ArticleListView.as_view(), name="articles"),
    path(
        "articles/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"
    ),
]
