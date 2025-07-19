from rest_framework import (
    viewsets,
)

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from apps.common.permissions import custom


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [custom.IsAuthorOrModeratorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
