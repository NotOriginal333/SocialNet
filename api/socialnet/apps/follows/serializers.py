from rest_framework import serializers

from apps.follows.models import Follow, FollowRecommendation
from apps.users.serializers import UserSerializer


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'followed_user']
        read_only_fields = ['id']

    def validate_followed_user(self, value):
        """Validate that user is not following themselves."""
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError("You cannot follow yourself.")
        return value

    def validate(self, attrs):
        """Validate that user is not already following another user."""
        user = self.context['request'].user
        followed = attrs.get('followed_user')

        if Follow.objects.filter(followed_user=followed, following_user=user).exists():
            raise serializers.ValidationError("You are already following this user.")

        return attrs

    def create(self, validated_data):
        validated_data['following_user'] = self.context['request'].user
        return super().create(validated_data)


class FollowRecommendationSerializer(serializers.ModelSerializer):
    recommended_users = UserSerializer(many=True)

    class Meta:
        model = FollowRecommendation
        fields = ['id', 'user', 'recommended_users', 'updated_at']
        read_only_fields = ['id']
