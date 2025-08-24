from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.images.models import UserImage


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object."""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'role', 'password', 'image_url', 'first_name', 'last_name', 'birth_date')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def get_image_url(self, obj):
        try:
            return obj.avatar.image_url
        except UserImage.DoesNotExist:
            return None

    def create(self, validated_data):
        """Create and return user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
