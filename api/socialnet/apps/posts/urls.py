from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostViewSet.as_view, name="posts")
]