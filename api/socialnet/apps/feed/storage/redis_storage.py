import redis
from .base import BaseFeedStorage


class RedisFeedStorage(BaseFeedStorage):
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def add_post(self, user_id: int, post_id: int, score: float) -> None:
        self.redis.zadd(f"feed:{user_id}", {str(post_id): score})

    def get_feed(self, user_id: int, limit: int = 30):
        return [int(pid) for pid in self.redis.zrevrange(f"feed:{user_id}", 0, limit - 1)]

    def clear_feed(self, user_id: int) -> None:
        self.redis.delete(f"feed:{user_id}")
