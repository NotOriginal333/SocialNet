from typing import List
from apps.feed.generator.scoring import base_score
from apps.posts.models import Post
from apps.follows.models import Follow


class FanOutFeedGenerator:
    def __init__(self, storage, super_node_threshold=100_000, fanout_chunk=5000):
        self.storage = storage
        self.super_node_threshold = super_node_threshold
        self.fanout_chunk = fanout_chunk

    def generate_for_post(self, post_id: int):
        """
        Main entrypoint:
        1. compute score
        2. check super-node threshold
        3. either push to trending or schedule fanout
        """
        post = Post.objects.only("id", "owner_id", "created_at", "likes_count").get(pk=post_id)
        score = base_score(post.created_at, getattr(post, "likes_count", 0))

        followers_qs = Follow.objects.filter(followed_user_id=post.owner_id).values_list("following_user_id", flat=True)
        followers_count = followers_qs.count()

        if followers_count >= self.super_node_threshold:
            self.storage.add_post("trending", post.id, score)
            return

        batch: List[int] = []
        for uid in followers_qs.iterator(chunk_size=self.fanout_chunk):
            batch.append(uid)
            if len(batch) >= self.fanout_chunk:
                self._fanout_batch(batch, post.id, score)
                batch = []

        if batch:
            self._fanout_batch(batch, post.id, score)

    def _fanout_batch(self, user_ids: List[int], post_id: int, score: float):
        """
        Internal: push post into a batch of user feeds
        """
        for uid in user_ids:
            self.storage.add_post(uid, post_id, score)
