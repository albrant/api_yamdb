from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': False},
            'email': {'required': True}
        }

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.first_name = validated_data.get(
            'first_name',
            instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name',
            instance.last_name
        )
        if instance.role == 'admin':
            instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'Выберите другой username'})
        return data


class UserAccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data
