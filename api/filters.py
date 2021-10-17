from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()

class GeolocationFilter(filters.FilterSet):
    min_distance = filters.NumberFilter(field_name="distance", lookup_expr='gte')
    max_distance = filters.NumberFilter(field_name="distance", lookup_expr='lte')

    class Meta:
        model = User
        fields = ['min_distance', 'max_distance']
