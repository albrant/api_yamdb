from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Comments, Genre, Review, Title

from .customviewset import CustomModelViewSet
from .filtersets import TitleFilter
from .permissions import IsAdminUserOrReadOnly, IsAdminOrAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('titles_reviews__score')).all()

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get("category")
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist("genre")
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrAuthorOrReadOnly
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, id=self.kwargs.get('title_id'))
        queryset = Review.objects.filter(title=title_id)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        # serializer.save(author=self.request.user)


class CommentsViewSet(CustomModelViewSet, viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
