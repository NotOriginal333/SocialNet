from rest_framework import permissions


class IsAuthenticatedAndRole(permissions.BasePermission):
    """
    Base permission that checks if user is authenticated
    and has one of the allowed roles.
    """

    allowed_roles = []

    def has_permission(self, request, view):
        return (
                bool(request.user and request.user.is_authenticated) and
                request.user.role in self.allowed_roles
        )


class IsAuthorOrRole(permissions.BasePermission):
    """
    Base permission for object-level access to authors or users with a specific role.
    """

    allowed_roles = []

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return (
                getattr(obj, 'author', None) == request.user or
                request.user.role in self.allowed_roles
        )


class IsOwnerOrRole(permissions.BasePermission):
    """
    Base permission for object-level access to owners or users with a specific role.
    """

    allowed_roles = []

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        return (
                getattr(obj, 'user', None) == request.user or
                request.user.role in self.allowed_roles
        )
