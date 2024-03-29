from django.db import models
from django.contrib.auth.models import User
from catalogue.models import Product

from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    def __str__(self):
        if self.parent:
            return f"reply by {self.user.username} for comment №{self.parent.id}"
        return f"comment №{self.id} by {self.user.username}"
