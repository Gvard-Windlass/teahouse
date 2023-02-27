from django import forms
from django.forms import ModelForm, Textarea
from .models import Comment


class CommentForm(ModelForm):
    next_page = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ["text", "next_page"]
        widgets = {"text": Textarea(attrs={"cols": 60, "rows": 3})}
        labels = {"text": ""}
