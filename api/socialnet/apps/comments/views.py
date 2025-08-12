from rest_framework import viewsets

from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
