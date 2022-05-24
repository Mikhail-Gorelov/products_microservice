from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'country')
    list_filter = ('country',)
    search_fields = ('country',)
