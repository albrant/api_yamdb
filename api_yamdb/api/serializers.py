from rest_framework import serializers
from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Titles
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comments, Titles
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['slug']
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='name',
        many=True
    )

    class Meta:
        fields = '__all__'
        extra_kwargs = {"description": {"required": False, "allow_null": True}}
        model = Titles


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_review(self, value):
        author = self.context['request'].user
        title_id = self.context['request'].parser_context['kwargs'].get('title_id')
        title = get_object_or_404(
            Titles,
            id=title_id
        )
        if (self.context['request'].method == 'POST'
                and title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(
                f'Отзыв на произведение {title.name} уже существует'
            )
        return value

    class Meta:
        fields = '__all__'
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comments


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)
        read_only_fields = ('username',)
