from django.contrib import admin
from . import models


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    pass
