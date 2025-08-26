from apps.interactions.tasks import update_interaction_counters


class InteractionCounterMixin:
    """Mixin to trigger counter updates after interaction changes."""

    def increment_counter(self, target, interaction_type: str):
        """
        Trigger async counter increment task for a target object.
        """
        update_interaction_counters.delay(
            target_model=target._meta.label,
            target_id=target.id,
            interaction_type=interaction_type,
            action="increment",
        )

    def decrement_counter(self, target, interaction_type: str):
        """
        Trigger async counter decrement task for a target object.
        """
        update_interaction_counters.delay(
            target_model=target._meta.label,
            target_id=target.id,
            interaction_type=interaction_type,
            action="decrement",
        )
