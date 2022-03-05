from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GenreViewSet, TitlesViewSet, ReviewViewSet, CommentsViewSet

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitlesViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentsViewSet,
    basename='comments'
)
# router.register('auth/signup/', SignupViewSet, basename='signup')
# router.register('auth/token/', TokenViewSet, basename='tokens')
router.register('users/', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
]
