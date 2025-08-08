from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from apps.images.models import UserImage, PostImage
from apps.images.serializers import UserImageSerializer, PostImageSerializer
from apps.images.tasks import generate_thumbnail_for_userimage, generate_thumbnail_for_postimage
from apps.images.services import get_image_storage
from apps.posts.models import Post


class BaseImageViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    lookup_field = 'pk'

    image_field_name = 'image'
    path_template = ''
    related_field = None
    thumbnail_task = None

    def get_storage_filename(self, instance, filename):
        return self.path_template.format(instance=instance, filename=filename)

    def save_file(self, instance, image):
        storage = get_image_storage()
        filename = self.get_storage_filename(instance, image.name)
        return storage.save(image, filename)

    def perform_create(self, serializer):
        related_value = self.get_related_value()

        image = self.request.FILES.get(self.image_field_name)
        print("Got image:", image)
        instance = serializer.save(**{self.related_field: related_value})
        instance.refresh_from_db()

        if image:
            image_url = self.save_file(instance, image)
            instance.image_url = image_url
            instance.save()
            self.thumbnail_task.delay(instance.id)

    def perform_update(self, serializer):
        image = self.request.FILES.get(self.image_field_name)
        instance = serializer.save()
        instance.refresh_from_db()

        if image:
            image_url = self.save_file(instance, image)
            instance.image_url = image_url
            instance.save()
            self.thumbnail_task.delay(instance.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if getattr(instance, self.related_field) != request.user:
            return Response(status=403)
        return super().destroy(request, *args, **kwargs)

    def get_related_value(self):
        raise NotImplementedError("Subclasses must implement get_related_value()")


class UserImageViewSet(BaseImageViewSet):
    serializer_class = UserImageSerializer
    queryset = UserImage.objects.all()

    image_field_name = 'image'
    path_template = "users/{instance.user.id}/avatar.jpg"
    related_field = 'user'
    thumbnail_task = generate_thumbnail_for_userimage
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserImage.objects.filter(user=self.request.user)

    def get_related_value(self):
        return self.request.user

    def perform_create(self, serializer):
        existing = self.get_queryset().first()
        if existing:
            serializer.instance = existing
            self.perform_update(serializer)
        else:
            super().perform_create(serializer)


class PostImageViewSet(BaseImageViewSet):
    serializer_class = PostImageSerializer
    queryset = PostImage.objects.all()

    image_field_name = 'image'
    path_template = "users/{instance.post.author.id}/posts/{instance.post.id}/{filename}"
    related_field = 'post'
    thumbnail_task = generate_thumbnail_for_postimage

    def get_queryset(self):
        return PostImage.objects.filter(post__author=self.request.user)

    def get_related_value(self):
        post_id = self.request.data.get("post")
        post = get_object_or_404(Post, id=post_id)
        if post.author != self.request.user:
            raise PermissionError("You can only upload to your own posts")
        return post
