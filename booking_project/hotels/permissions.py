from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет администраторам делать все,
    а другим пользователям только читать данные.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff  # Проверка на администратора

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет пользователю редактировать или удалять
    только свои бронирования.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user  # Проверка на совпадение пользователя
