from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Comment
from catalogue.models import Product
from .forms import CommentForm


class CommentsCreateView(LoginRequiredMixin, View):
    login_url = "/login"

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        product = get_object_or_404(Product, pk=kwargs.get("product_id"))
        next_page = request.POST.get("next_page")
        reply_target = kwargs.get("comment_id")

        if comment_form.is_valid():
            comment: Comment = comment_form.save(commit=False)
            comment.product = product
            comment.user = request.user
            if reply_target:
                comment.parent = Comment.objects.get(pk=reply_target)
            comment.save()

            messages.success(request, "Комментарий добавлен")
        else:
            messages.success(request, "Ошибка при добавлении комментария")

        return redirect(next_page)
