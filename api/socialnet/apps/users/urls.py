from django.urls import path
from django.http import JsonResponse

from . import views

app_name = 'users'


def oauth_callback(request):  # for test purposes only!
    return JsonResponse({
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
    })


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path("callback/", oauth_callback, name="oauth_callback"),  # for test purposes only!
]
