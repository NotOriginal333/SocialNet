from rest_framework import (
    viewsets,
    permissions
)

from apps.follows.models import Follow
from apps.follows.serializers import FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(following_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(following_user=self.request.user)
