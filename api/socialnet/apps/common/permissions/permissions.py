from rest_framework.permissions import BasePermission, SAFE_METHODS

from .constants import (
    ROLE_ADMIN,
    ROLE_MODERATOR,
)


class RoleScopePermission(BasePermission):
    """
    Base permission that checks if user is authenticated
    and has one of the allowed roles.
    """

    allowed_roles = []

    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        pass
