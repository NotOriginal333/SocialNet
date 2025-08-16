from rest_framework import serializers

from apps.posts.models import Post
from apps.images.serializers import PostImageSerializer


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'content', 'images', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
