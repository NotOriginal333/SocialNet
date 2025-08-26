from enum import Enum


class InteractionType(str, Enum):
    VIEW = "view"
    LIKE = "like"
    DISLIKE = "dislike"
    REPOST = "repost"
    SAVE = "save"

    @classmethod
    def choices(cls):
        """Return choices tuple for Django model fields"""
        return [(i.value, i.value.capitalize()) for i in cls]