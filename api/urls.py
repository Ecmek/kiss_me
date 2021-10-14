from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet

router = routers.DefaultRouter()
router.register('clients/create', UserViewSet, basename='user_create')

urlpatterns = [
    path('', include(router.urls)),
]
