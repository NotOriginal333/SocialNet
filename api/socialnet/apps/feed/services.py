import os
import redis

from apps.feed.storage.composite import CompositeFeedStorage
from apps.feed.storage.redis_storage import RedisFeedStorage
from apps.feed.storage.db_storage import DBFeedStorage

from apps.feed.generator.fanout import FanOutFeedGenerator


def get_feed_storage():
    redis_client = redis.Redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
                                        decode_responses=True)
    return CompositeFeedStorage([
        RedisFeedStorage(redis_client),
        DBFeedStorage(),
    ])


def get_feed_generator():
    return FanOutFeedGenerator(get_feed_storage())
