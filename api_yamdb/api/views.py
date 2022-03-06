from urllib import response
from django.conf import settings
from rest_framework.response import Response
from rest_framework import filters, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminUserOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from .serializers import (CategorySerializer, GenreSerializer,
                          TitlesSerializer, ReviewSerializer,
                          CommentsSerializer, UserSerializer,
                          UserCreationSerializer)
from .filtersets import TitlesFilter
from users.models import User
# from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from reviews.models import Category, Genre, Review, Titles, Comments
from .customviewset import CustomModelViewSet

# User = get_user_model()


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


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [TitlesFilter]


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


class SignupViewSet(viewsets.ModelViewSet):
    pass


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user, code_create = User.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Applying code',
        f'Your code {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
