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


class FollowRecommendation(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    recommended_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='recommended_to'
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recommendations for {self.user}"
