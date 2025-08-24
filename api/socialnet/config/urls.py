from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from oauth2_provider import urls as oauth2_urls

from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})


urlpatterns = [
    path('o/', include(oauth2_urls)),
    path('admin/', admin.site.urls),
    path('csrf/', get_csrf),
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
    path('interactions/', include('apps.interactions.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
