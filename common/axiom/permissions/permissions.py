class Permission:
    allowed_scopes: list[str] = []


class IsAdminPermission(Permission):
    allowed_scopes = ["admin"]


class IsAdminOrModeratorPermission(Permission):
    allowed_scopes = ["admin", "moderator"]


class IsAuthenticatedPermission(Permission):
    allowed_scopes = ["admin", "moderator", "user"]


class AllowAnyPermission(Permission):
    allowed_scopes = ["admin", "moderator", "user", "guest"]
