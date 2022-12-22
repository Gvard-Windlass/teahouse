from django.db import models

class Article(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='article_images/', null=True, blank=True)
    summary = models.TextField()
    body = models.TextField()
    publication_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} | by {self.author}'