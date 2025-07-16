from .base import IsAuthenticatedAndRole, IsAuthorOrRole, IsOwnerOrRole


class IsAdmin(IsAuthenticatedAndRole):
    """Allows access only to users with the 'admin' role."""
    allowed_roles = ['admin']


class IsModerator(IsAuthenticatedAndRole):
    """Allows access to users with 'moderator' or 'admin' roles."""
    allowed_roles = ['moderator', 'admin']


class IsPremiumUser(IsAuthenticatedAndRole):
    """Allows access to users with 'premium', 'moderator', or 'admin' roles."""
    allowed_roles = ['premium', 'moderator', 'admin']


class IsAuthorOrAdminOrReadOnly(IsAuthorOrRole):
    """Allows edit access to authors or admins. Read-only for others."""
    allowed_roles = ['admin']


class IsOwnerOrModerator(IsOwnerOrRole):
    """Allows access to owners or moderators/admins."""
    allowed_roles = ['moderator', 'admin']


class IsAuthorOrModeratorOrAdminOrReadOnly(IsAuthorOrRole):
    """Allows editing to author, moderator, or admin. Read-only for others."""
    allowed_roles = ['moderator', 'admin']
