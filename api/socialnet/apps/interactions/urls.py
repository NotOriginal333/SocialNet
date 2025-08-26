from rest_framework.routers import DefaultRouter

from apps.interactions.views import InteractionViewSet

router = DefaultRouter()

router.register(r'', InteractionViewSet, basename='interactions')

urlpatterns = router.urls


