from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Разрешение для доступа только пользователям с ролью 'admin'.
    """

    def has_permission(self, request, view):
        # Разрешить доступ, если пользователь аутентифицирован и имеет роль 'admin'
        return request.user and request.user.is_authenticated and request.user.role == 'admin'
