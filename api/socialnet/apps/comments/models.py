from django.db import models
from django.conf import settings


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def is_root(self):
        """Checks that comment have a parent comment."""
        return self.parent is None

    def __str__(self):
        return f"Comment author: {self.owner.username}, post {self.post.id}, at {self.created_at:%Y-%m-%d %H:%M}"
