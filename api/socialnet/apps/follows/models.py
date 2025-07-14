from django.db import models
from django.conf import settings


class Follow(models.Model):
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        ordering = ['followed_user']
        constraints = [
            models.UniqueConstraint(
                fields=['followed_user', 'following_user'],
                name='unique_follow_relationship'
            )
        ]

    def __str__(self):
        return f'User: {self.following_user}, Follows: {self.followed_user}'
