from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'bio')
    search_fields = ('first_name',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
