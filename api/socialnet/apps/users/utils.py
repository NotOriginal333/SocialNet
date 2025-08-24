ROLE_SCOPES = {
    'user': ['read', 'create'],
    'moderator': ['read', 'create', 'update', 'delete', 'moderate'],
    'admin': ['read', 'create', 'update', 'delete', 'moderate', 'admin'],
}


def get_scopes_for_role(role: str):
    """Return list of scopes based on user role."""
    return ROLE_SCOPES.get(role, ['read'])
