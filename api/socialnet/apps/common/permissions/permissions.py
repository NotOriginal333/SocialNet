from rest_framework.permissions import BasePermission, SAFE_METHODS


class RoleScopePermission(BasePermission):
    """
       Permission that:
       - Allows anyone to read (GET, HEAD, OPTIONS).
       - Allows only authenticated users to create (POST).
       - Allows object owners, moderators, and admins to edit/delete.
       - Allows only admins to perform admin-level actions (e.g., deleting users).
       Also checks OAuth2 token scopes and user roles.
       """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        token = getattr(request, 'auth', None)
        if not token or not hasattr(token, 'scope'):
            return False
        token_scopes = token.scope.split()

        if request.method == 'POST':
            return 'create' in token_scopes or 'admin' in token_scopes

        if request.method in ('PUT', 'PATCH'):
            return any(s in token_scopes for s in ('update', 'moderate', 'admin'))

        if request.method == 'DELETE':
            return any(s in token_scopes for s in ('delete', 'moderate', 'admin'))

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        user_role = getattr(user, 'role', 'user')

        if hasattr(obj, 'owner') and obj.owner == user:
            return True

        if user_role == 'admin':
            return True

        if user_role == 'moderator' and request.method in ('PUT', 'PATCH', 'DELETE'):
            return True

        return False
