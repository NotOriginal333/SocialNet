from celery import shared_task
from django.apps import apps

from apps.common.enums import InteractionType

INTERACTION_FIELD_MAP = {
    InteractionType.VIEW: "views_count",
    InteractionType.LIKE: "likes_count",
    InteractionType.DISLIKE: "dislikes_count",
    InteractionType.REPOST: "reposts_count",
    InteractionType.SAVE: "saves_count",
}


@shared_task
def update_interaction_counters(target_model: str, target_id: int, interaction_type: str, action: str):
    """
    Update counters for target objects.
    interaction_type must be one of InteractionType values.
    """
    model = apps.get_model(target_model)
    target = model.objects.filter(id=target_id).first()
    if not target:
        return

    try:
        enum_type = InteractionType(interaction_type)
    except ValueError:
        return

    field_name = INTERACTION_FIELD_MAP.get(enum_type)
    if not field_name or not hasattr(target, field_name):
        return

    value = getattr(target, field_name, 0)
    if action == "increment":
        setattr(target, field_name, value + 1)
    elif action == "decrement" and value > 0:
        setattr(target, field_name, value - 1)

    target.save(update_fields=[field_name])
