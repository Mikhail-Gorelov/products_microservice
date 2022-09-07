from django.db.models import QuerySet
from django_filters import rest_framework as filters

from product import models
from product.models import Product


class ProductsFilter(filters.FilterSet):
    price_from = filters.NumberFilter(method='price_from_filter')
    price_to = filters.NumberFilter(method='price_to_filter')
    sort_by_rating = filters.BooleanFilter(method="sort_by_rating_filter")
    is_bestseller = filters.BooleanFilter(field_name='is_bestseller')
    category = filters.NumberFilter(method='category_filter')
    category_slug = filters.CharFilter(method='category_slug_filter')

    def sort_by_rating_filter(self, queryset: QuerySet[Product], name: str, value: bool):
        filter_rating = '-rating' if value is True else 'created'
        return queryset.order_by(filter_rating)

    def price_from_filter(self, queryset: QuerySet[Product], name: str, value: int):
        product_variant = models.ProductVariantChannelListing.objects.filter(
            cost_price__gte=value,
            visible_in_listings=True
        )
        return queryset.filter(
            variants__channel_listings__in=product_variant
        )

    def price_to_filter(self, queryset: QuerySet[Product], name: str, value: int):
        product_variant = models.ProductVariantChannelListing.objects.filter(
            cost_price__lte=value,
            visible_in_listings=True
        )
        return queryset.filter(
            variants__channel_listings__in=product_variant
        )

    def category_filter(self, queryset: QuerySet[Product], name: str, value: int):
        product_type = models.ProductType.objects.filter(category__id=value)
        return queryset.filter(product_type__in=product_type)

    def category_slug_filter(self, queryset: QuerySet[Product], name: str, value: int):
        product_type = models.ProductType.objects.filter(category__slug=value)
        return queryset.filter(product_type__in=product_type)
