from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or (
                request.user.is_staff and request.user.is_authenticated):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False
