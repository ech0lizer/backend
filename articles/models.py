from django.db import models
from authentication.models import User


class Article(models.Model):
    title = models.CharField(unique=True, db_index=True, max_length=255)
    text = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
