from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

admin.site.site_header = 'Спринт 10 команды 14 кагорты 27 Яндекс Практикума'
admin.site.index_title = 'Админка'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/', include('api.urls', namespace='api')),
    path('api/', include('users.urls', namespace='users')),
]
