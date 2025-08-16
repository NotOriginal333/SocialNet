from datetime import timedelta
from django.utils import timezone

from rest_framework.test import APIClient
from oauth2_provider.models import AccessToken, Application

from apps.common.test import create_user


def setup_api_client():
    """Helper function to set up api client, token and user for tests."""
    user = create_user(
        email='user@example.com',
        password='testpass',
        username='usertestname',
        first_name='name',
        last_name='surname'
    )
    app = Application.objects.create(
        name="Test App",
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
        user=user,
    )
    token = AccessToken.objects.create(
        user=user,
        application=app,
        token="testtoken123",
        expires=timezone.now() + timedelta(days=1),
        scope="read create update delete",
    )
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.token}")
    return user, client, token
