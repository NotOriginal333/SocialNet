from rest_framework.viewsets import ModelViewSet

from .models import Interaction
from .serializers import InteractionSerializer
from .mixins import InteractionCounterMixin


class InteractionViewSet(InteractionCounterMixin, ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        interaction, created = serializer.save_or_get(user=self.request.user)
        if created:
            self.increment_counter(interaction.target, interaction.interaction_type)

    def perform_destroy(self, instance):
        self.decrement_counter(instance.target, instance.interaction_type)
        instance.delete()
