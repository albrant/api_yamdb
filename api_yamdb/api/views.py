from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Titles, Comments
from users.models import User
from .customviewset import CustomModelViewSet
from .serializers import ReviewSerializer, CommentsSerializer, UserSerializer


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


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
