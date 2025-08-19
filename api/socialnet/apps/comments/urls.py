from django.urls import path

from apps.comments.views import CommentListCreateView, CommentDetailView

urlpatterns = [
    path("posts/<int:post_id>/", CommentListCreateView.as_view(), name="post-comments"),
    path("<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
