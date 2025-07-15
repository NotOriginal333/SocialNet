from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs'
    ),
    path('users/', include('apps.users.urls')),
    path('posts/', include('apps.posts.urls')),
    path('comments/', include('apps.comments.urls')),
    path('follows/', include('apps.follows.urls')),
    path('images/', include('apps.images.urls')),
]
