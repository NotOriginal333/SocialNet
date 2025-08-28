from rest_framework import (
    viewsets,
    generics
)
from rest_framework.exceptions import ValidationError

from apps.follows.models import Follow, FollowRecommendation
from apps.follows.serializers import FollowSerializer, FollowRecommendationSerializer
from apps.follows.tasks import update_recommendations_for_user


def create_follow(following, followed):
    Follow.objects.create(following_user=following, followed_user=followed)
    update_recommendations_for_user.delay(following.id)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.queryset.filter(following_user=self.request.user)

    def perform_create(self, serializer):
        followed_user = serializer.validated_data.get("followed_user")

        if followed_user == self.request.user:
            raise ValidationError("You cannot follow yourself.")

        if Follow.objects.filter(following_user=self.request.user, followed_user=followed_user).exists():
            raise ValidationError("You are already following this user.")

        create_follow(self.request.user, followed_user)


class FollowRecommendationView(generics.RetrieveAPIView):
    serializer_class = FollowRecommendationSerializer

    def get_object(self):
        recommendation, _ = FollowRecommendation.objects.get_or_create(user=self.request.user)
        return recommendation
