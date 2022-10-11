from django.conf import settings
from rest_framework import serializers

from actions.models import Like
from api.v1.product.services import ProductService
from product import models
from product.models import Category
from channel.models import Channel


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
    is_liked = serializers.SerializerMethodField('get_is_liked')

    def get_media(self, obj):
        return ProductService.get_media_of_product(obj=obj, request=self.context['request'])

    def get_full_price(self, obj):
        return ProductService.get_full_price_of_product(obj=obj, request=self.context['request'])

    def get_variants_count(self, obj):
        return ProductService.get_variants_count(obj=obj, request=self.context['request'])

    def get_is_liked(self, obj):
        if not self.context['request'].remote_user:
            return Like.objects.filter(product=obj).exists()
        return Like.objects.filter(user_id=self.context['request'].remote_user.id, product=obj).exists()

    class Meta:
        model = models.Product
        fields = ("id", "name", "media", "full_price", "rating", "description", "variants_count", "is_liked")


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
        return ProductService.get_media_for_variants(obj=obj, request=self.context['request'])

    def get_variants(self, obj):
        return VariantsSerializer(ProductService.get_variants(obj=obj, request=self.context['request']), many=True).data

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


class ProductVariantDetailSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    full_price = serializers.SerializerMethodField()
    description = serializers.CharField(source='product.description')
    is_liked = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_media(self, obj):
        return settings.MEDIA_URL + str(obj.variant_media.all().first().media.media_file)

    def get_full_price(self, obj):
        return obj.channel_listings.all().first().cost_price

    def get_is_liked(self, obj):
        if not self.context['request'].remote_user:
            return Like.objects.filter(product=obj.product).exists()
        return Like.objects.filter(user_id=self.context['request'].remote_user.id, product=obj.product).exists()

    def get_rating(self, obj):
        return obj.product.rating

    class Meta:
        model = models.ProductVariant
        fields = ('id', 'name', 'media', 'full_price', 'description', 'is_liked', 'rating')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'slug', 'description', 'background_image')


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'slug', 'currency_code', 'country')


class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ("name",)


class TotalPositionsSerializer(serializers.Serializer):
    variant_ids = serializers.ListField(child=serializers.IntegerField())
