from rest_framework import serializers

from apps.images.models import UserImage
from apps.images.models import PostImage


class BaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['image_url', 'thumbnail_url', 'uploaded_at']
        read_only_fields = ['image_url', 'thumbnail_url', 'uploaded_at']
        abstract = True


class UserImageSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        fields = BaseImageSerializer.Meta.fields + ['user']
        read_only_fields = ['user']
        model = UserImage


class PostImageSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        fields = BaseImageSerializer.Meta.fields + ['post']
        read_only_fields = ['post']
        model = PostImage
