from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'avatar', 'gender', 'first_name', 'last_name', 'email')

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
