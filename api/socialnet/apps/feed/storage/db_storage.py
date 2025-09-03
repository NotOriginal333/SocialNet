from .base import BaseFeedStorage
from apps.feed.models import UserFeed


class DBFeedStorage(BaseFeedStorage):
    def add_post(self, user_id: int, post_id: int, score: float) -> None:
        UserFeed.objects.create(user_id=user_id, post_id=post_id, score=score)

    def get_feed(self, user_id: int, limit: int = 30):
        return list(
            UserFeed.objects.filter(user_id=user_id)
            .order_by("-score")[:limit]
            .values_list("post_id", flat=True)
        )

    def clear_feed(self, user_id: int) -> None:
        UserFeed.objects.filter(user_id=user_id).delete()
