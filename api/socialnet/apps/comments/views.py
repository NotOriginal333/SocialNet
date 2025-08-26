from rest_framework import generics
from django.shortcuts import get_object_or_404

from apps.posts.models import Post
from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.comments.tasks import update_post_comments_count


class CommentListCreateView(generics.ListCreateAPIView):
    """
    GET: List all comments for a given post.
    POST: Create a new comment (or reply) for a given post.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id, parent__isnull=True)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(owner=self.request.user, post=post)
        update_post_comments_count(post.id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single comment.
    PUT/PATCH: Update your comment (or admin can edit any).
    DELETE: Delete your comment (or admin can delete any).
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        super().perform_destroy(instance)
        update_post_comments_count(post.id)
