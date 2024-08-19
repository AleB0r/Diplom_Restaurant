from rest_framework import permissions


class IsAdminOrPurchaser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_role = getattr(request.user, 'role', None)
        return user_role in ['admin', 'buyer']
