from rest_framework import serializers

from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'owner', 'post', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'post', 'owner', 'created_at', 'updated_at']
