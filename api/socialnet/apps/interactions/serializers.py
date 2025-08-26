from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import Interaction
from apps.common.rules import INTERACTION_RULES


class InteractionSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    object_id = serializers.IntegerField(write_only=True)
    content_type_input = serializers.CharField(write_only=True)

    class Meta:
        model = Interaction
        fields = ['id', 'user', 'interaction_type', 'content_type', 'content_type_input', 'object_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at', 'content_type']

    def get_content_type(self, obj):
        if isinstance(obj, dict):
            ct = obj.get('content_type')
        else:
            ct = getattr(obj, 'content_type', None)

        if not ct:
            return None
        return f"{ct.app_label}.{ct.model}"

    def validate(self, attrs):
        """
        Ensure interaction is allowed for the given target model.
        """
        ct_str = attrs.get('content_type_input')
        if not ct_str:
            raise serializers.ValidationError({"content_type_input": "This field is required."})

        try:
            app_label, model = ct_str.split(".")
        except ValueError:
            raise serializers.ValidationError({"content_type_input": "Invalid format. Use 'app_label.model'."})

        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({"content_type_input": "Invalid content type."})

        interaction_type = attrs.get("interaction_type")
        if not interaction_type:
            raise serializers.ValidationError({"interaction_type": "This field is required."})

        allowed = INTERACTION_RULES.get(f"{app_label}.{model.lower()}", set())
        if interaction_type not in allowed:
            raise serializers.ValidationError({
                "interaction_type": f"Interaction '{interaction_type}' is not allowed for {ct_str}."
            })

        attrs['content_type'] = content_type
        attrs.pop('content_type_input')
        return attrs

    def save_or_get(self, user):
        """
        Automatically assign user and returns existing Interaction if present, else create a new one.
        """
        data = self.validated_data.copy()
        content_type = data.pop('content_type')
        object_id = data.pop('object_id')
        interaction_type = data.pop('interaction_type')

        interaction, created = Interaction.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=object_id,
            interaction_type=interaction_type
        )
        return interaction, created
