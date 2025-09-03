"""
Base score calculation: recency + popularity.
Affinity (user-specific boost) is applied at read time for small candidate set.
"""

import math
from django.utils import timezone


def base_score(created_at, likes_count: int, now=None) -> float:
    """
    Compute a 'base' score independent of a specific reader.
    """
    if now is None:
        now = timezone.now()
    hours = (now - created_at).total_seconds() / 3600.0
    recency_score = math.exp(-hours / 24.0)
    popularity_score = math.log1p(max(0, likes_count))
    # weights
    w_recency = 0.6
    w_pop = 0.4
    return w_recency * recency_score + w_pop * popularity_score
