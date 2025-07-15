from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404

from apps.images.models import UserImage, PostImage
from apps.images.serializers import UserImageSerializer, PostImageSerializer
from apps.images.tasks import generate_thumbnail_for_userimage, generate_thumbnail_for_postimage
from apps.images.services import get_image_storage
from apps.posts.models import Post


class UserImageViewSet(viewsets.ModelViewSet):
    serializer_class = UserImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return UserImage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        existing = UserImage.objects.filter(user=self.request.user).first()
        if existing:
            existing.delete()

        image = self.request.FILES.get('image')
        storage = get_image_storage()
        filename = f"users/{self.request.user.id}/avatar.jpg"
        path = storage.save(image, filename)

        instance = serializer.save(user=self.request.user, image_url=path)
        generate_thumbnail_for_userimage.delay(instance.id)

    def perform_update(self, serializer):
        image = self.request.FILES.get('image')
        if image:
            storage = get_image_storage()
            filename = f"users/{self.request.user.id}/avatar.jpg"
            path = storage.save(image, filename)
            serializer.save(image_url=path)
        else:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=403)
        return super().destroy(request, *args, **kwargs)


class PostImageViewSet(viewsets.ModelViewSet):
    serializer_class = PostImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return PostImage.objects.filter(post__author=self.request.user)

    def perform_create(self, serializer):
        post_id = self.request.data.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        if post.author != self.request.user:
            raise PermissionError("You can only upload to your own posts")

        image = self.request.FILES.get('image')
        storage = get_image_storage()
        filename = f"posts/{post.id}/{image.name}"
        path = storage.save(image, filename)

        instance = serializer.save(post=post, image_url=path)
        generate_thumbnail_for_postimage.delay(instance.id)

    def perform_update(self, serializer):
        image = self.request.FILES.get('image')
        if image:
            storage = get_image_storage()
            instance = self.get_object()
            filename = f"posts/{instance.post.id}/{image.name}"
            path = storage.save(image, filename)
            serializer.save(image_url=path)
        else:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.post.author != request.user:
            return Response(status=403)
        return super().destroy(request, *args, **kwargs)
