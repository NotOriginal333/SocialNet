from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import RoleScopePermission
from apps.posts.models import Post
from .services import get_feed_storage
from .serializers import PostListSerializer


class FeedView(APIView):
    permission_classes = (IsAuthenticated, RoleScopePermission)

    def get(self, request):
        """
        Returns user feed.
        Supports query parameter 'limit'.
        """
        limit = int(request.query_params.get("limit", 30))
        storage = get_feed_storage()

        feed_items = storage.get_feed(user_id=request.user.id, limit=limit)

        post_ids = feed_items
        posts_qs = Post.objects.filter(id__in=post_ids).order_by("-created_at")

        serializer = PostListSerializer(posts_qs, many=True, context={"request": request})
        return Response(serializer.data)
