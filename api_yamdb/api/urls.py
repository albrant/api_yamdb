from django.urls import include, path
from rest_framework import routers

#from .views import ReviewsViewSet

app_name = 'api'

router = routers.DefaultRouter()
#router.register('reviews', ReviewsViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),
]
