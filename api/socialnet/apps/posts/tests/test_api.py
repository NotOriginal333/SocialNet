from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from oauth2_provider.models import AccessToken, Application

from apps.common.test import create_user, create_superuser, setup_api_client
from apps.posts.models import Post
from apps.images.models import PostImage


class TestPostsAPI(APITestCase):
    """Tests for posts API."""

    def setUp(self):
        self.user, self.client, self.token = setup_api_client()

    def test_create_post_sets_owner(self):
        """Test that post owner is always the logged-in user."""
        payload = {
            "content": "My test post",
            "owner": 999,
        }
        url = reverse("posts-list")
        res = self.client.post(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=res.data["id"])
        self.assertEqual(post.owner, self.user)
        self.assertEqual(post.content, payload["content"])

    def test_user_cannot_update_or_delete_others_post(self):
        """Test that a user cannot update or delete another user's post."""
        other_user = create_user(
            email='other@example.com',
            password='otherpass',
            username='otheruser'
        )
        other_post = Post.objects.create(owner=other_user, content="Other's content")

        url = reverse("posts-detail", args=[other_post.id])
        res_update = self.client.put(url, {"content": "Hacked content"}, format="json")
        self.assertEqual(res_update.status_code, status.HTTP_403_FORBIDDEN)

        res_delete = self.client.delete(url)
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_or_delete_own_post(self):
        """Test that a user can update or delete their own post."""
        post = Post.objects.create(owner=self.user, content="Original content")

        url = reverse("posts-detail", args=[post.id])
        res_update = self.client.put(url, {"content": "Updated content"}, format="json")
        self.assertEqual(res_update.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.content, "Updated content")

        res_delete = self.client.delete(url)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())

    def test_admin_can_update_or_delete_any_post(self):
        """Test that admin can update or delete any user's post."""

        other_user = create_user(
            email='other@example.com',
            password='otherpass',
            username='otheruser',
            first_name='Other',
            last_name='User'
        )
        post = Post.objects.create(owner=other_user, content='Other user post')

        admin_user = create_superuser()

        app = Application.objects.create(
            name="Admin App",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=admin_user
        )
        token = AccessToken.objects.create(
            user=admin_user,
            application=app,
            token="admintoken123",
            expires=timezone.now() + timedelta(days=1),
            scope="read create update delete admin"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.token}")

        url = reverse("posts-detail", args=[post.id])

        payload = {"content": "Updated by admin"}
        res_update = self.client.patch(url, payload, format="json")
        self.assertEqual(res_update.status_code, status.HTTP_200_OK)

        post.refresh_from_db()
        self.assertEqual(post.content, payload["content"])

        res_delete = self.client.delete(url)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())


class TestPostsWithImagesAPI(APITestCase):
    """Tests for posts API with images."""

    def setUp(self):
        self.user, self.client, self.token = setup_api_client()

    def test_create_post_with_image(self):
        """Test creating a post with an image sets the relation correctly."""
        post = Post.objects.create(owner=self.user, content="Post with image")

        post_image = PostImage.objects.create(
            post=post,
            image_url="http://example.com/test.jpg",
            thumbnail_url="http://example.com/test_thumb.jpg"
        )

        self.assertTrue(post.images.exists())
        self.assertIn(post_image, post.images.all())


class TestPostsReadOnlyAPI(APITestCase):
    """Tests for retrieving posts and images without authentication."""

    def setUp(self):
        self.user = create_user(
            email="user@example.com",
            password="testpass",
            username="usertest"
        )
        self.post = Post.objects.create(owner=self.user, content="Test post content")

        self.post_image = PostImage.objects.create(
            post=self.post,
            image_url="http://example.com/test.jpg",
            thumbnail_url="http://example.com/test_thumb.jpg"
        )

    def test_get_post_list(self):
        """Test retrieve list of posts with images."""
        url = reverse("posts-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) > 0)

        post_data = res.data[0]
        self.assertEqual(post_data["content"], self.post.content)

        images = post_data.get("images", [])
        self.assertTrue(any(img["image_url"] == self.post_image.image_url for img in images))
        self.assertTrue(any(img["thumbnail_url"] == self.post_image.thumbnail_url for img in images))

    def test_get_post_detail(self):
        """Test retrieve single post with images."""
        url = reverse("posts-detail", args=[self.post.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["content"], self.post.content)

        images = res.data.get("images", [])
        self.assertTrue(any(img["image_url"] == self.post_image.image_url for img in images))
        self.assertTrue(any(img["thumbnail_url"] == self.post_image.thumbnail_url for img in images))