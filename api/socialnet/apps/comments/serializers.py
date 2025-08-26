from rest_framework import serializers

from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'owner', 'likes_count', 'dislikes_count', 'replies',
                  'parent', 'post', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'replies', 'likes_count', 'dislikes_count',
                            'post', 'created_at', 'updated_at']

    def get_replies(self, obj):
        """Return only direct replies (1 level)."""
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True, context=self.context).data

    def validate_parent(self, value):
        """
        Ensure only one level of replies is allowed:
        - parent must be a root comment (no parent itself).
        """
        if value and value.parent:
            raise serializers.ValidationError(
                "Replies can only be made to root comments."
            )
        return value
