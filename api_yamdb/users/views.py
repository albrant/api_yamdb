from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdminUserOrReadOnly

from .models import User
from .serializers import (UserAccessTokenSerializer, UserCreationSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
        else:
            serializer = UserSerializer(self.request.user,
                                        data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    user, code_created = User.objects.get_or_create(
        email=email, username=username)
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
    return Response(
        'Код подтверждения выслан на указанный адрес электронной почты',
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def getjwttoken(request):
    serializer = UserAccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    confirmation_code = serializer.data['confirmation_code']
    user = get_object_or_404(
        User, email=email, confirmation_code=confirmation_code)
    default_token_generator.check_token(user, confirmation_code)
    token = AccessToken.for_user(user)
    serializer.data['token'] = token
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
