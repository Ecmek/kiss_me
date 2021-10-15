from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import MatchAPIView, UserViewSet

router = routers.DefaultRouter()
router.register('clients/create', UserViewSet, basename='user_create')

urlpatterns = [
    path('', include(router.urls)),
    path('clients/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('clients/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('clients/<int:id>/match/', MatchAPIView.as_view()),
]
