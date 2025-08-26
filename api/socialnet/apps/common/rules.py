from .enums import InteractionType

INTERACTION_RULES = {
    'posts.post': {InteractionType.VIEW, InteractionType.LIKE, InteractionType.DISLIKE,
                   InteractionType.REPOST, InteractionType.SAVE},
    'comments.comment': {InteractionType.LIKE, InteractionType.DISLIKE},
}


def is_allowed_interaction(target_type: str, interaction_type: InteractionType) -> bool:
    """Check if interaction is allowed for the given target"""
    return interaction_type in INTERACTION_RULES.get(target_type, set())
