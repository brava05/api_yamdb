from rest_framework import permissions


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False

        return (obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                )

class AuthorAdminModeratorOrReadAndPost(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            return request.user.is_authenticated
        
        if not request.user.is_authenticated:
            return False

        return (obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                )

class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False
        return request.user.role == 'admin'


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser is True
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser is True
        )

        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin'
        )


# class AuthenticatedOrReadOnly(permissions.BasePermission):

#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )

