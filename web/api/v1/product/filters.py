from django.db.models import QuerySet

from channel.models import Channel
from product import models
from product.models import Product
from django_filters import rest_framework as filters


class ProductsFilter(filters.FilterSet):
    price_from = filters.NumberFilter(method='price_from_filter')
    price_to = filters.NumberFilter(method='price_to_filter')
    sort_by_rating = filters.BooleanFilter(method="sort_by_rating_filter")

    def sort_by_rating_filter(self, queryset: QuerySet[Product], name: str, value: bool):
        filter_rating = '-rating' if value is True else 'created'
        return queryset.order_by(filter_rating)

    def price_from_filter(self, queryset: QuerySet[Product], name: str, value: int):
        channel = Channel.objects.filter(**self.request.COOKIES)
        product_variant = models.ProductVariantChannelListing.objects.filter(
            channel__in=channel,
            cost_price__gte=value,
            visible_in_listings=True
        )
        return queryset.filter(
            variants__channel_listings__in=product_variant,
            is_bestseller=True
        ).distinct()

    def price_to_filter(self, queryset: QuerySet[Product], name: str, value: int):
        channel = Channel.objects.filter(**self.request.COOKIES)
        product_variant = models.ProductVariantChannelListing.objects.filter(
            channel__in=channel,
            cost_price__lte=value,
            visible_in_listings=True
        )
        return queryset.filter(
            variants__channel_listings__in=product_variant,
            is_bestseller=True
        ).distinct()
