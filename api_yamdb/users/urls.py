from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import UserViewSet, getjwttoken, signup

app_name = 'users'

users_router = DefaultRouter()
users_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('api/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify/',
         TokenVerifyView.as_view(),
         name='token_verify'),
    path('v1/auth/token/', getjwttoken, name='token'),
    path('v1/auth/signup/', signup),
    path('v1/', include(users_router.urls)),
]
