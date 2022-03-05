from django_filters.rest_framework import CharFilter, FilterSet
from reviews.models import Titles


class TitlesFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Titles
        fields = ['year', 'genre__slug', 'category__slug']
