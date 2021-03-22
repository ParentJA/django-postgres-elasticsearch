from django.contrib import admin

from .models import Wine


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    fields = ('id', 'country', 'description', 'points', 'price', 'variety', 'winery',)
    list_display = ('id', 'country', 'points', 'price', 'variety', 'winery',)
    list_filter = ('country', 'variety', 'winery',)
    ordering = ('variety',)
    readonly_fields = ('id',)
