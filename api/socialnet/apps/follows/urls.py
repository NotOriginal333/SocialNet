from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.follows.views import (
    FollowViewSet,
    FollowRecommendationView,
    FollowUserView,
)

router = DefaultRouter()
router.register(r'', FollowViewSet, basename='follows')

urlpatterns = [
    path('recommendations/', FollowRecommendationView.as_view(), name='follow-recommendations'),
    path('<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
] + router.urls
