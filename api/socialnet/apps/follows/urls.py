from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.follows.views import (
    FollowViewSet,
    FollowRecommendationView,
)

router = DefaultRouter()
router.register(r'', FollowViewSet, basename='follows')

urlpatterns = [
    path('recommendations/', FollowRecommendationView.as_view(), name='follow-recommendations'),
] + router.urls
