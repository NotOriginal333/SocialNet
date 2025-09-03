from typing import List


class BaseFeedStorage:
    def add_post(self, user_id: int, post_id: int, score: float) -> None:
        raise NotImplementedError

    def get_feed(self, user_id: int, limit: int = 30) -> List[int]:
        raise NotImplementedError

    def clear_feed(self, user_id: int) -> None:
        raise NotImplementedError
