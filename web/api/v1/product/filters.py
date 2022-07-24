from django.db.models import QuerySet
from product.models import Product
from django_filters import rest_framework as filters


class ProductsFilter(filters.FilterSet):
    sort_by_rating = filters.BooleanFilter(method="sort_by_rating_filter")

    # min_price = filters.NumberFilter(method="min_price_filter")
    # max_price = filters.NumberFilter(method="max_price_filter")

    def sort_by_rating_filter(self, queryset: QuerySet[Product], name: str, value: bool):
        filter_rating = '-rating' if value is True else 'created'
        return queryset.order_by(filter_rating)

    # def min_price_filter(self, queryset: QuerySet[Product], name: str, value: int):
    #     return queryset.order_by(filter_rating)
