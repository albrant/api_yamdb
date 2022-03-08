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
        if request.user and request.user.is_authenticated:
            if (request.method == 'POST' and request.user.is_authenticated
                    or request.user.is_staff or request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user):
                return True
        elif request.method in SAFE_METHODS:
            return True

    # message = status.HTTP_403_FORBIDDEN
    # edit_methods = ("PUT", "PATCH", "DELETE",)
    #
    # def has_object_permission(self, request, view, obj):
    #     user = request.user
    #     if request.method == "POST":
    #         return user == user.is_authenticated
    #     if request.method in SAFE_METHODS:
    #         return True
    #     if request.method in self.edit_methods:
    #         return (
    #             user.is_moderator()
    #             or user.is_admin()
    #             or user == obj.author
    #         )
    #     return False
