from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import User


class IsAdministrator(permissions.BasePermission):
    """
    Allows access only to an administrator or a superuser.
    """
    def __check_is_admin(self, request):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.role == User.ADMIN
                or request.user.is_superuser
            )
        )

    def has_permission(self, request, view):
        return self.__check_is_admin(request)

    def has_object_permission(self, request, view, obj):
        return self.__check_is_admin(request)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission allowing only an author of an object
    or a superuser to edit it.
    Assumes the model instance has an `author` attribute.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user
                and request.user.is_authenticated
            )
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user == obj.author
                or request.user.is_superuser
            )
        )


class IsModerator(permissions.BasePermission):
    """
    Allows access only to a moderator or a superuser.
    """
    def __check_is_moderator(self, request):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.role == User.MODERATOR
                or request.user.is_superuser
            )
        )

    def has_permission(self, request, view):
        return self.__check_is_moderator(request)

    def has_object_permission(self, request, view, obj):
        return self.__check_is_moderator(request)


class ReadOnly(permissions.BasePermission):
    """
    Allows anyone to access with a read-only request
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
