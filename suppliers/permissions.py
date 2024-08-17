from rest_framework import permissions


class IsAdminOrPurchaser(permissions.BasePermission):
    """
    Позволяет доступ только пользователям с ролью 'admin' или 'purchaser'.
    """

    def has_permission(self, request, view):
        # Позволяет доступ к API только для методов GET, HEAD, OPTIONS без проверки роли
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверка роли пользователя
        user_role = getattr(request.user, 'role', None)
        return user_role in ['admin', 'buyer']
