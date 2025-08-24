from rest_framework.permissions import BasePermission, SAFE_METHODS


def has_permission_for_action(user, obj, token_scopes, action):
    is_owner = hasattr(obj, "owner") and obj.owner == user
    is_privileged = "admin" in token_scopes or "moderate" in token_scopes

    return action in token_scopes and (is_owner or is_privileged)


class RoleScopePermission(BasePermission):
    """
    Custom permission class that enforces both read safety and scope-based access.
    - SAFE methods (GET, HEAD, OPTIONS) are always allowed.
    - Write methods require valid token scopes.
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
        """
        Additional object-level checks:
        - SAFE methods are always allowed.
        - Owner of the object can modify it.
        """
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        if hasattr(obj, 'owner') and obj.owner == user:
            return True

        token = getattr(request, 'auth', None)
        if not token or not hasattr(token, 'scope'):
            return False
        token_scopes = token.scope.split()

        if request.method in ("PUT", "PATCH"):
            return has_permission_for_action(user, obj, token_scopes, "update")

        if request.method == "DELETE":
            return has_permission_for_action(user, obj, token_scopes, "delete")

        return False
