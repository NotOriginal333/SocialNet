from rest_framework import serializers
from apps.posts.models import Post


class PostListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author_username', 'content', 'created_at', 'likes_count']
