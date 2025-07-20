from celery import shared_task
from django.contrib.auth import get_user_model
from .services import generate_recommendations_for_user

User = get_user_model()


@shared_task
def update_recommendations_for_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return
    generate_recommendations_for_user(user)
