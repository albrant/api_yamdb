from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['year', 'genre__slug', 'category__slug']
