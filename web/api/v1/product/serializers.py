from rest_framework import serializers
from django.conf import settings
from product import models
from product.models import Category


class HotProductsSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    full_price = serializers.DecimalField(decimal_places=2, max_digits=8)

    class Meta:
        model = models.ProductVariant
        fields = ("id", "name", "media", "full_price")

    def get_media(self, obj):
        return settings.MEDIA_URL + obj.media


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductType
        fields = ("name", "kind", "has_variants", "is_shipping_required", "is_digital")


class ProductDetailUnitSerializer(serializers.ModelSerializer):
    breadcrumbs = serializers.SerializerMethodField('get_breadcrumbs')
    media = serializers.SerializerMethodField('get_media')

    def get_breadcrumbs(self, obj):
        category: Category = obj.product_type.category
        breadcrumbs = list(category.get_ancestors().values('name', 'slug'))
        breadcrumbs.append({
            'name': category.name,
            'slug': category.slug
        })
        return breadcrumbs

    def get_media(self, obj):
        return [settings.MEDIA_URL + i[0] for i in obj.media.all().values_list('media_file')]

    class Meta:
        model = models.Product
        fields = ("description", "breadcrumbs", "weight", "rating", "slug", "media")


class ProductDetailSerializer(serializers.ModelSerializer):
    product = ProductDetailUnitSerializer()
    price = serializers.CharField()
    cost_price = serializers.CharField()


    class Meta:
        model = models.ProductVariant
        fields = ("id", "name", "price", "cost_price", "product")


class ProductListUnitSerializer(serializers.ModelSerializer):
    breadcrumbs = serializers.SerializerMethodField('get_breadcrumbs')

    def get_breadcrumbs(self, obj):
        category: Category = obj.product_type.category
        breadcrumbs = list(category.get_ancestors().values('name', 'slug'))
        breadcrumbs.append({
            'name': category.name,
            'slug': category.slug
        })
        return breadcrumbs

    class Meta:
        model = models.Product
        fields = ("description", "breadcrumbs", "slug")


class ProductListSerializer(serializers.ModelSerializer):
    product = ProductListUnitSerializer()
    product_media = serializers.CharField()

    class Meta:
        model = models.ProductVariant
        fields = ("id", "product", "name", "product_media")
