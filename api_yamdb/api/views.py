from rest_framework import filters, viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUserOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from .serializers import CategorySerializer, GenreSerializer, TitlesSerializer, ReviewSerializer, CommentsSerializer
from .filtersets import TitleFilter, CategoryFilter, GenreFilter
from reviews.models import Category, Genre, Titles, Review, Titles, Comments
from .customviewset import CustomModelViewSet


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('category__name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('genre__name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [TitleFilter, CategoryFilter, GenreFilter]


class ReviewViewSet(CustomModelViewSet, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = self.kwargs.get('title_id')
        get_object_or_404(Titles, id=title)
        queryset = Review.objects.filter(title=title)
        return queryset


class CommentsViewSet(CustomModelViewSet, viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review = self.kwargs.get('review_id')
        get_object_or_404(Review, id=review)
        queryset = Comments.objects.filter(review=review)
        return queryset
