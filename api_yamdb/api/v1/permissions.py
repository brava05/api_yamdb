from rest_framework import permissions
from users.models import User


class AdminOnly(permissions.BasePermission):
    """
    Права доступа только у админа.
    """
    # def has_permission(self, request, view):
    #     return (
    #         request.user.is_authenticated
    #         and request.user.role == User.ADMINISTRATOR
    #         or request.user.is_superuser
    #     )


    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == User.ADMINISTRATOR
            or request.user.is_superuser is True
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права доступа:
    чтение для всех, изменение только для администратора.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == User.ADMINISTRATOR
                or request.user.is_superuser)
            or (request.user.is_authenticated
                and request.user.is_superuser)
        )

class IsAuthorAdminModeratorOrReadAndPost(permissions.BasePermission):
    """Постить могут все, а исправлять только админы, модераторы и авторы"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        return request.user.is_authenticated and (
            request.user == obj.author
            or request.user.role == User.MODERATOR
            or request.user.role == User.ADMINISTRATOR
        )
