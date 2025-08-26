from rest_framework import serializers

from apps.posts.models import Post
from apps.images.serializers import PostImageSerializer


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'content', 'images', 'comments_count',
                  'views_count', 'likes_count', 'dislikes_count', 'reposts_count',
                  'saves_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'comments_count', 'views_count',
                            'likes_count', 'dislikes_count', 'reposts_count',
                            'saves_count', 'updated_at']
