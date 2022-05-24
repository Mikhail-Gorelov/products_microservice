from rest_framework import serializers
from product import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ("name", "description", "background_image")

class ProductTypeSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = models.ProductType
        fields = ("name", "category", "kind", "has_variants", "is_shipping_required", "is_digital")

class ProductSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer()
    class Meta:
        model = models.Product
        fields = ("name", "product_type", "description", "weight", "rating")

class ProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = models.ProductVariant
        fields = ("name", "product", "media", "track_inventory", "is_preorder", "preorder_end_date", "preorder_threshold")

class HotProductsSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer()
    class Meta:
        model = models.ProductVariantChannelListing
        fields =("product_variant", "available_to_purchase", "price", "cost_price")
