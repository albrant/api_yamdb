from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comments, Genre, Review, Title


class CustomModelViewSet:
    # def perform_create(self, serializer):
    #     # надо написать про авторизацию
    #     # if not self.request.user.is_authenticated:
    #     #     raise PermissionDenied(
    #     #         'Для выполнения данного действия '
    #     #         'необходимо авторизироваться.'
    #     #     )
    #     title_id = self.kwargs.get('title_id')
    #     title = get_object_or_404(Titles, id=title_id)
    #     serializer.save(author=self.request.user, title=title)
    #     # serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if (serializer.instance.author != self.request.user
                or self.request.user.is_admin is False
                or self.request.user.is_moderator is False):
            raise PermissionDenied(
                'У вас недостаточно прав '
                'для выполнения данного действия.'
            )
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if (instance.author != self.request.user
                or self.request.user.is_admin is False
                or self.request.user.is_moderator is False):
            raise PermissionDenied(
                'У вас недостаточно прав '
                'для выполнения данного действия.'
            )
        super().perform_destroy(instance)
