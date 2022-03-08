from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import status

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_admin:
            return True


class IsAdminOrAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)

        return bool(request.user and (
                request.user == obj.author or
                request.user.is_moderator or
                request.user.is_admin))

