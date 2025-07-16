from rest_framework import (
    viewsets,
    permissions
)

from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.common.permissions import custom


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [custom.IsAuthorOrModeratorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
