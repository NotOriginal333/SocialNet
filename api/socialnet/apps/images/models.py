from django.db import models
from apps.posts.models import Post
from django.contrib.auth import get_user_model


class BaseImage(models.Model):
    image_url = models.CharField(max_length=500, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=500, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


User = get_user_model()


class UserImage(BaseImage):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')

    def __str__(self):
        return f"Avatar for {self.user.username}"


class PostImage(BaseImage):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for post {self.post.id}"
