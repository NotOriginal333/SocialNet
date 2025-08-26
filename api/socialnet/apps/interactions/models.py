from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.exceptions import ValidationError

from apps.common.enums import InteractionType
from apps.common.rules import INTERACTION_RULES


class Interaction(models.Model):
    """
    Represents a user interaction on a generic target object.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="interactions",
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    interaction_type = models.CharField(
        max_length=20,
        choices=InteractionType.choices,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "content_type", "object_id", "interaction_type"],
                name="unique_user_interaction"
            )
        ]

    def clean(self):
        """
        Validate if this interaction is allowed for the target model.
        """
        model_key = f"{self.content_type.app_label}.{self.content_type.model}"
        allowed = INTERACTION_RULES.get(model_key, set())

        if self.interaction_type not in allowed:
            raise ValidationError(
                f"Interaction '{self.interaction_type}' is not allowed for {model_key}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} {self.interaction_type} {self.target}"
