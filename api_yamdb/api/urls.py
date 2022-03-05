from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet, GenreViewSet, TitlesViewSet,
                    ReviewViewSet, CommentsViewSet, UserViewSet,
                    SignupViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitlesViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register('auth/signup', SignupViewSet, basename='signup')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    # path('auth/token/', TokenView, name='token'),
    path('v1/', include(router.urls)),
]
