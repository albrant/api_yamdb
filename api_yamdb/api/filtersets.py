from rest_framework import filters
from reviews.models import Category, Genre, Titles


class TitleFilter(filters.FilterSet):
    class Meta:
        model = Titles
        fields = ('name', 'year')


class CategoryFilter(filters.FilterSet):

    class Meta:
        model = Category
        fields = ('slug',)


class GenreFilter(filters.FilterSet):

    class Meta:
        model = Genre
        fields = ('slug',)
