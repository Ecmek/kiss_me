from django.contrib.auth import get_user_model
from rest_framework import serializers

from match.models import Match

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'avatar', 'gender', 'first_name', 'last_name', 'email', 'password')

    def validate_avatar(self, avatar):
        if not avatar:
            return avatar
        # 8MB
        MAX_FILE_SIZE = 8388608
        # 100kB
        MIN_FILE_SIZE = 102400
        if avatar.size > MAX_FILE_SIZE:
            raise serializers.ValidationError(
                'Загружаемый аватар больше 8 МБ'
            )
        if avatar.size < MIN_FILE_SIZE:
            raise serializers.ValidationError(
                'Загружаемый аватар меньше 100 кБ'
            )
        return avatar


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
    mark = serializers.BooleanField()

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
