from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg
from reviews.models import Category, Comments, Genre, Review, Title

from .customviewset import CustomModelViewSet
from .filters import TitleFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminUserOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('category__name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('genre__name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializer
    permission_classes = [IsAdminUserOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    # def get_queryset(self):
    #     return Title.objects.annotate(
    #         rating=Avg('title_review__score')).all()

    # def perform_create(self, serializer):
    #     category = get_object_or_404(
    #         Category, slug=self.request.data.get("category")
    #     )
    #     genre = Genre.objects.filter(
    #         slug__in=self.request.data.getlist("genre")
    #     )
    #     serializer.save(category=category, genre=genre)

    # def perform_update(self, serializer):
    #     self.perform_create(serializer)


class ReviewViewSet(CustomModelViewSet, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = self.kwargs.get('title_id')
        get_object_or_404(Title, id=title)
        queryset = Review.objects.filter(title=title)
        return queryset


class CommentsViewSet(CustomModelViewSet, viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review = self.kwargs.get('review_id')
        get_object_or_404(Review, id=review)
        queryset = Comments.objects.filter(review=review)
        return queryset
