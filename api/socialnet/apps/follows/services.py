from django.db import models
from apps.users.models import User
from apps.follows.models import Follow, FollowRecommendation


def generate_recommendations_for_user(user: User):
    followed_ids = user.following.values_list('followed_user_id', flat=True)
    exclude_ids = list(followed_ids) + [user.id]

    recommended = (
        User.objects.exclude(id__in=exclude_ids)
        .annotate(followers_count=models.Count('followers'))
        .order_by('-followers_count')[:10]
    )

    rec, _ = FollowRecommendation.objects.get_or_create(user=user)
    rec.recommended_users.set(recommended)
    rec.save()


def create_follow(following, followed):
    from apps.follows.tasks import update_recommendations_for_user
    Follow.objects.create(following_user=following, followed_user=followed)
    update_recommendations_for_user.delay(following.id)
