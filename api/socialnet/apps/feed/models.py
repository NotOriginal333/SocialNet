from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class UserFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    post_id = models.BigIntegerField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post_id'),)
        indexes = [
            models.Index(fields=['user', '-score']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'User: {self.user.username},post id: {self.post_id} (score: {self.score})'
