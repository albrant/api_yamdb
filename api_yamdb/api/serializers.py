from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comments


class ReviewSerializer(serializers.ModelSerializer):
    # title = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    # title = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comments
