ROLE_USER = "user"
ROLE_PREMIUM = "premium_user"
ROLE_MODERATOR = "moderator"
ROLE_ADMIN = "admin"

ROLES = [
    (ROLE_USER, "User"),
    (ROLE_PREMIUM, "Premium User"),
    (ROLE_MODERATOR, "Moderator"),
    (ROLE_ADMIN, "Admin"),
]

SCOPES = {
    'read': 'Read access',
    'write': 'Write access',
    'moderate': 'Moderate content',
    'admin': 'Full admin access',
}
