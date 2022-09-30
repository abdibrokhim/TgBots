from django.contrib import admin
from .models import TGClient, TGClientQuery


class TGClientAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('tg_id',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


class TGClientQueryAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'query', 'created_at')
    list_filter = ('tg_id', 'query', 'created_at',)
    search_fields = ('tg_id', 'query',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    unique_together = ('tg_id', 'query',)


admin.site.register(TGClient, TGClientAdmin)
admin.site.register(TGClientQuery, TGClientQueryAdmin)
