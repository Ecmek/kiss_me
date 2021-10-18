from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CategoryListViewSet, MatchAPIView, ProductsListViewSet,
                    UserListViewSet, UserViewSet, get_geolocation,
                    set_geolocation)

router = routers.DefaultRouter()
router.register('clients/create', UserViewSet, basename='user_create')
router.register('list', UserListViewSet, basename='users_list')
router.register('category', CategoryListViewSet, basename='category')
router.register(r'products/(?P<category_slug>[\w\@\.\+\-]+)', ProductsListViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('clients/<int:id>/match/', MatchAPIView.as_view(), name='match'),
    path('clients/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('clients/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('clients/get_geolocation/', get_geolocation, name='get_geolocation'),
    path('clients/set_geolocation/', set_geolocation, name='set_geolocation'),
]
