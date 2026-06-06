from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем (GET), 
    но изменение (POST, PUT, PATCH, DELETE) — только администраторам.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)