from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    # image = models.ImageField(upload_to='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # comments = models.ManyToManyField(Comment, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Created by: {self.author.email}, at {self.created_at:%Y-%m-%d %H:%M}"
