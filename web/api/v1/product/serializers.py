from django.db.models import OuterRef, Subquery
from rest_framework import serializers
from django.conf import settings

from channel.models import Channel
from product import models
from product.models import Category


class VariantsSerializer(serializers.ModelSerializer):
    full_price = serializers.DecimalField(decimal_places=2, max_digits=8)
    weight = serializers.DecimalField(decimal_places=1, max_digits=5)
    slug = serializers.SlugField(max_length=255)
    variant_media = serializers.SerializerMethodField('get_variant_media')

    def get_variant_media(self, obj):
        return settings.MEDIA_URL + obj.variant_media

    class Meta:
        model = models.ProductVariant
        fields = ("id", "name", "weight", "slug", "full_price", "variant_media")


class ProductSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField('get_media')
    full_price = serializers.SerializerMethodField('get_full_price')
    variants_count = serializers.SerializerMethodField('get_variants_count')

    def get_media(self, obj):
        return settings.MEDIA_URL + str(obj.variants.first().media.all().first().media_file)

    def get_full_price(self, obj):
        return obj.variants.first().channel_listings.first().cost_price

    def get_variants_count(self, obj):
        variant = models.ProductVariant.objects.filter(product=obj, channel_listings__visible_in_listings=True)
        return variant.count()

    class Meta:
        model = models.Product
        fields = ("id", "name", "media", "full_price", "rating", "description", "variants_count")


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductType
        fields = ("name", "kind", "has_variants", "is_shipping_required", "is_digital")


class ProductDetailUnitSerializer(serializers.ModelSerializer):
    breadcrumbs = serializers.SerializerMethodField('get_breadcrumbs')
    media = serializers.SerializerMethodField('get_media')
    variants = serializers.SerializerMethodField('get_variants')

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

    def get_variants(self, obj):
        channel_dict = {
            'country': self.context['request'].COOKIES.get('country'),
            'currency_code': self.context['request'].COOKIES.get('currency_code'),
        }
        channel = Channel.objects.filter(**channel_dict)
        product_variant = models.ProductVariantChannelListing.objects.filter(
            channel__in=channel,
            visible_in_listings=True,
            product_variant__product=obj
        )
        name = models.ProductVariant.objects.filter(id=OuterRef('product_variant_id')).values('name')
        full_price = models.ProductVariant.objects.filter(id=OuterRef('product_variant_id')).values(
            'channel_listings__cost_price')
        weight = models.ProductVariant.objects.filter(id=OuterRef('product_variant_id')).values('weight')
        slug = models.ProductVariant.objects.filter(id=OuterRef('product_variant_id')).values('slug')
        variant_media = models.ProductVariant.objects.filter(id=OuterRef('product_variant_id')).values(
            'media__media_file')
        serializer_input = product_variant.select_related('product_variant', ).all().annotate(
            name=Subquery(name),
            full_price=Subquery(full_price),
            weight=Subquery(weight),
            slug=Subquery(slug),
            variant_media=Subquery(variant_media)
        )
        return VariantsSerializer(serializer_input, many=True).data

    class Meta:
        model = models.Product
        fields = ("id", "description", "breadcrumbs", "rating", "media", "variants")


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


class ProductsSerializer(serializers.Serializer):
    products = serializers.ListSerializer(child=serializers.IntegerField())
