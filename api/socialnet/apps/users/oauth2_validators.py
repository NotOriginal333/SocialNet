from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    def get_available_scopes(self, client_id=None, request=None, *args, **kwargs):
        print("it works somehow!")
        if request and request.user and request.user.is_authenticated:
            user = request.user
            if user.role == 'admin':
                return ['read', 'create', 'update', 'delete', 'moderate', 'admin']
            elif user.role == 'moderator':
                return ['read', 'moderate']
            else:
                return ['read', 'create', 'update', 'delete']
        return ['read']
