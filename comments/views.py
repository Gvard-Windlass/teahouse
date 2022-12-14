import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from .models import Comment
from catalogue.models import Product
from .forms import CommentForm


class CommentsCreateView(View):
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        product = Product.objects.get(pk=kwargs.get('product_id'))
        next_page = request.POST.get('next_page')
        
        if comment_form.is_valid():
            comment: Comment = comment_form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()

            messages.success(request, 'Комментарий добавлен')
        else:
            messages.success(request, 'Ошибка при добавлении комментария')
        
        return redirect(next_page)
        