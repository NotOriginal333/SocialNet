from django.test import TestCase

from apps.common.test import create_user
from apps.posts.models import Post


class PostModelTests(TestCase):
    """Tests model for posts."""

    def setUp(self):
        self.user = create_user()

    def test_create_post(self):
        """Test that a post can be successfully created."""
        post = Post.objects.create(owner=self.user, content="Test content")

        self.assertEqual(post.owner, self.user)
        self.assertEqual(post.content, "Test content")
        self.assertIsNotNone(post.created_at)

    def test_update_post_content(self):
        """Test updating the content of a post."""
        post = Post.objects.create(owner=self.user, content="Old content")
        post.content = "New content"
        post.save()

        updated_post = Post.objects.get(id=post.id)
        self.assertEqual(updated_post.content, "New content")

    def test_delete_post(self):
        """Test deleting a post."""
        post = Post.objects.create(owner=self.user, content="Some content")
        post_id = post.id
        post.delete()

        self.assertFalse(Post.objects.filter(id=post_id).exists())

    def test_post_str_method(self):
        """Test the string representation of a post."""
        post = Post.objects.create(owner=self.user, content="Hello world")
        self.assertIn("Post owner: ", str(post))
        self.assertIn(self.user.email, str(post))
