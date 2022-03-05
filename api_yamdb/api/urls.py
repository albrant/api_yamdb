from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentsViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
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
