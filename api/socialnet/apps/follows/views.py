from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets,
    permissions,
    generics
)
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.follows.models import Follow, FollowRecommendation
from apps.follows.serializers import FollowSerializer, FollowRecommendationSerializer
from apps.follows.services import create_follow
from apps.users.models import User


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowRecommendationSerializer

    def get_object(self):
        recommendation, _ = FollowRecommendation.objects.get_or_create(user=self.request.user)
        return recommendation


class FollowUserView(APIView):
    def post(self, request, user_id):
        followed = get_object_or_404(User, id=user_id)
        follow = create_follow(request.user, followed)
        return Response({"status": "followed", "id": follow.id})
