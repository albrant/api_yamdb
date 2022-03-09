from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdmin, ReadOnly, IsAuthor, IsModerator, IsAdminUserOrReadOnly

from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

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
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )

    # def get_queryset(self):
    #     title = self.kwargs.get('title_id')
    #     get_object_or_404(Title, id=title)
    #     queryset = Review.objects.filter(title=title)
    #     return queryset


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    # def get_queryset(self):
    #     review = self.kwargs.get('review_id')
    #     get_object_or_404(Review, id=review)
    #     queryset = Comments.objects.filter(review=review)
    #     return queryset
