from math import acos, cos, radians, sin

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from match.models import Match
from products.models import Category, Product
from users.models import Geolocation

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'avatar', 'gender', 'first_name', 'last_name', 'email', 'password')

    def validate_avatar(self, avatar):
        if not avatar:
            return avatar
        if avatar.size > settings.MAX_FILE_SIZE:
            raise serializers.ValidationError(
                'Загружаемый аватар больше 8 МБ'
            )
        if avatar.size < settings.MIN_FILE_SIZE:
            raise serializers.ValidationError(
                'Загружаемый аватар меньше 100 кБ'
            )
        return avatar


class UserListSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'avatar', 'gender', 'first_name', 'last_name', 'email', 'distance',)

    def get_distance(self, obj):
        return obj.distance

class MatchSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    matching = serializers.SlugRelatedField(
        slug_field='email', required=False,
        queryset=User.objects.all()
    )

    class Meta:
        model = Match
        fields = ('user', 'matching', 'mark')

    def create(self, validated_data):
        return Match.objects.create(**validated_data)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        user = self.context['request'].user
        matching = self.context['matching']

        if Match.objects.filter(user=user, matching=matching).exists():
            raise serializers.ValidationError(
                'Запись с таким совпадинем есть в БД, можно ее обновить'
            )

        if user == matching:
            raise serializers.ValidationError(
                'Нельзя давать оценку на самого себя'
            )

        return data


class GeolocationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Geolocation
        fields = ('user', 'latitude', 'longitude',)

    def create(self, validated_data):
        geolocation, created = Geolocation.objects.get_or_create(
            user=validated_data['user']
        )
        geolocation.latitude = validated_data['latitude']
        geolocation.longitude = validated_data['longitude']
        geolocation.save()
        return geolocation


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
