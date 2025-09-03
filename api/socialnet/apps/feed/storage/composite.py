from .base import BaseFeedStorage


class CompositeFeedStorage(BaseFeedStorage):
    def __init__(self, storages):
        self.storages = storages

    def add_post(self, user_id, post_id, score):
        for s in self.storages:
            s.add_post(user_id, post_id, score)

    def get_feed(self, user_id, limit=30):
        return self.storages[0].get_feed(user_id, limit=limit)
