from django.contrib.auth import get_user_model


def create_user(email='user@example.com', password='testpass123', **params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password, **params)


def create_superuser(email='admin@example.com', password='password', **params):
    """Create and return a new superuser."""
    return get_user_model().objects.create_superuser(email, password, **params)
