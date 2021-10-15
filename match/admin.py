from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Match

User = get_user_model()


class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'matching', 'mark', 'mark_time',
    )
    search_fields = ('user',)
    list_filter = ('mark_time',)
    empty_value_display = '-пусто-'


admin.site.register(Match, MatchAdmin)
