from django.contrib import admin

from .models import Category, Genre, Comments, Titles, Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'description')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug', 'description')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'description')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug', 'description')


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name', 'category')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'category')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    empty_value_display = '-пусто-'
    list_editable = ('text', 'author', 'score')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'text', 'pub_date')
    search_fields = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Review, ReviewAdmin)
