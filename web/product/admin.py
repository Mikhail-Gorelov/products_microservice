from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from . import models


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    readonly_fields = ('slug',)

    def get_readonly_fields(self, request, obj=None):
        return [] if obj else self.readonly_fields


@admin.register(models.Category)
class CategoryAdmin(TreeAdmin):
    list_display = ('id', 'name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    form = movenodeform_factory(models.Category)
    readonly_fields = ('slug',)

    def get_readonly_fields(self, request, obj=None):
        return [] if obj else self.readonly_fields


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    readonly_fields = ('slug',)

    def get_readonly_fields(self, request, obj=None):
        return [] if obj else self.readonly_fields


@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('media',)


@admin.register(models.ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ('id',)
    search_fields = ('id',)


@admin.register(models.ProductVariantChannelListing)
class ProductVariantChannelListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_variant', 'channel')
    list_filter = ('id',)
    search_fields = ('id',)


@admin.register(models.VariantMedia)
class VariantMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'variant', 'media')
    list_filter = ('id',)
    search_fields = ('id',)
