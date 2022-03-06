from rest_framework.permissions import SAFE_METHODS, IsAdminUser


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_staff:
            return True
