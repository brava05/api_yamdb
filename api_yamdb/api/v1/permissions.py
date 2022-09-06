from rest_framework import permissions


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser is True
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == 'admin')
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
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )
