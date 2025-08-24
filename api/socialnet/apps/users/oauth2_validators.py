from oauth2_provider.oauth2_validators import OAuth2Validator

from apps.users.utils import get_scopes_for_role


class CustomOAuth2Validator(OAuth2Validator):
    def save_bearer_token(self, token, request, *args, **kwargs):
        """
        Automatically set token scope according to user's role.
        Ignore scope from request.
        """
        if request.user:
            role_scopes = get_scopes_for_role(getattr(request.user, 'role', 'user'))
            token['scope'] = ' '.join(role_scopes)

        super().save_bearer_token(token, request, *args, **kwargs)
