from celery import shared_task

from .services import get_feed_storage, get_feed_generator

STORAGE = get_feed_storage()
GENERATOR = get_feed_generator()


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def post_created_fanout(self, post_id: int):
    """
    Celery entrypoint.
    Uses FanOutFeedGenerator to fanout the post to followers.
    """
    GENERATOR.generate_for_post(post_id)
