from django.db.models import Exists, OuterRef, Count

from apps.users.models import User
from apps.follows.models import Follow, FollowRecommendation


def generate_recommendations_for_user(user: User):
    following_exists = Follow.objects.filter(
        following_user=user, followed_user=OuterRef('pk')
    )

    recommended = (
        User.objects
        .annotate(already_followed=Exists(following_exists))
        .filter(already_followed=False)
        .exclude(id=user.id)
        .annotate(followers_count=Count('followers', distinct=True))
        .order_by('-followers_count')[:10]
    )

    rec, _ = FollowRecommendation.objects.get_or_create(user=user)
    rec.recommended_users.set(recommended)
    rec.save()
