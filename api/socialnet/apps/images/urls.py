from rest_framework.routers import DefaultRouter
from .views import UserImageViewSet, PostImageViewSet

router = DefaultRouter()
router.register(r'avatars', UserImageViewSet, basename='avatar')
router.register(r'post-images', PostImageViewSet, basename='post_image')

urlpatterns = router.urls
