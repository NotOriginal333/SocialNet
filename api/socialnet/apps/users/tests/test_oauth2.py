from urllib.parse import urlparse, parse_qs
import base64
import hashlib
import secrets

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from oauth2_provider.models import get_application_model
from rest_framework.test import APIClient

User = get_user_model()
Application = get_application_model()


class OAuth2FlowTests(TestCase):
    """
    Test the OAuth2 flow.
    """

    def setUp(self):
        """
        Set up a user and two application types (public and confidential).
        """
        self.user_password = "testpass123"
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password=self.user_password,
            first_name="test",
            last_name="test"
        )

        self.public_app = Application.objects.create(
            name="Test Public App",
            client_id="client_id_123",
            user=self.user,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris="http://localhost:8000/users/callback/",
            skip_authorization=True,
        )

        self.confidential_app = Application.objects.create(
            name="Confidential App",
            client_id="confidential_client_123",
            client_secret="confidential_secret_123",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris="http://localhost:8000/users/callback/",
            skip_authorization=True,
        )

        self.token_client = Client()

    def _get_authorization_code(self, app, code_challenge=None):
        """
        Returns the authorization code for the given OAuth2 application.
        This method now correctly handles both public (PKCE) and confidential clients.
        """
        logged_in = self.client.login(email=self.user.email, password=self.user_password)
        self.assertTrue(logged_in, "Failed to log in user")

        params = {
            "response_type": "code",
            "client_id": app.client_id,
            "redirect_uri": app.redirect_uris.split()[0],
            "scope": "read",
        }

        self.assertIsNotNone(code_challenge, "PKCE flow requires a code challenge.")
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"

        response = self.client.get("/o/authorize/", params)

        self.assertEqual(response.status_code, 302, msg=f"Authorize failed: {response.content.decode()}")
        redirect_url = response["Location"]

        qs = parse_qs(urlparse(redirect_url).query)
        self.assertIn("code", qs, msg=f"No code in redirect URL: {redirect_url}")

        return qs["code"][0]

    def test_full_oauth2_flow_with_pkce(self):
        """
        Test the PKCE flow for a public client.
        """
        code_verifier = secrets.token_urlsafe(43)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).rstrip(b'=').decode()

        code = self._get_authorization_code(self.public_app, code_challenge=code_challenge)
        self.assertIsNotNone(code, "Authorization code not obtained for PKCE")

        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.public_app.redirect_uris,
            "client_id": self.public_app.client_id,
            "code_verifier": code_verifier,
        }

        resp = self.token_client.post(
            "/o/token/",
            data=token_data,
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, 200, resp.content)
        access_token = resp.json()["access_token"]

        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        api_response = api_client.get("/users/me/")
        self.assertEqual(api_response.status_code, 200)

    # def test_oauth2_flow_confidential_client(self):
    #     """
    #     Test the standard authorization code flow for a confidential client.
    #     """
    #     code_verifier = secrets.token_urlsafe(43)
    #     code_challenge = base64.urlsafe_b64encode(
    #         hashlib.sha256(code_verifier.encode()).digest()
    #     ).rstrip(b'=').decode()
    #
    #     code = self._get_authorization_code(self.confidential_app, code_challenge=code_challenge)
    #     self.assertIsNotNone(code, "Authorization code not obtained for confidential client")
    #
    #     token_data = {
    #         "grant_type": "authorization_code",
    #         "code": code,
    #         "redirect_uri": self.confidential_app.redirect_uris,
    #         "client_id": self.confidential_app.client_id,
    #         "client_secret": self.confidential_app.client_secret,
    #         "code_verifier": code_verifier,
    #     }
    #
    #     resp = self.token_client.post(
    #         "/o/token/",
    #         data=token_data,
    #         content_type="application/json"
    #     )
    #
    #     self.assertEqual(resp.status_code, 200, resp.content)
    #     access_token = resp.json()["access_token"]
    #
    #     api_client = APIClient()
    #     api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    #     api_response = api_client.get("/users/me/")
    #     self.assertEqual(api_response.status_code, 200)

    def test_invalid_token_access(self):
        """
        Test that an invalid token returns 401 Unauthorized.
        """
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION="Bearer WRONGTOKEN")
        resp = api_client.get("/users/me/")
        self.assertEqual(resp.status_code, 401)
