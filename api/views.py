from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
