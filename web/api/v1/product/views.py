from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from product.pagination import BaseProductsPagination
from product import models, choices
from django.db.models import Sum, Subquery, OuterRef, Count
from channel.models import Channel
from product.models import Category, Product, ProductVariant
from . import serializers
from .services import ProductService


class HotProductsView(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = BaseProductsPagination
    serializer_class = serializers.HotProductsSerializer

    def get_queryset(self):
        if not ProductService.is_channel_exists(self.channel_cookie):
            return None
        channel = Channel.objects.filter(**self.channel_cookie)
        product_variant = models.ProductVariantChannelListing.objects.filter(
            channel__in=channel,
            is_bestseller=True,
            visible_in_listings=True
        )
        name = models.ProductVariant.objects.filter(id=OuterRef('product_variant_id')).values('name')
        media = models.ProductVariant.objects.filter(id=OuterRef('product_variant_id')).values('media__media_file')[:1]
        full_price = models.ProductVariant.objects.filter(id=OuterRef('product_variant_id')).values('channel_listings__cost_price')
        return product_variant.select_related('product_variant', ).all().annotate(
            name=Subquery(name),
            media=Subquery(media),
            full_price=Subquery(full_price)
        )

    def list(self, request, *args, **kwargs):
        self.channel_cookie = {k: v[0] for k, v in dict(request.data).items()}
        return super().list(request, *args, **kwargs)


class CategoriesView(GenericAPIView):
    def get(self, request):
        return Response(Category.dump_bulk())


class ProductDetailView(RetrieveAPIView):
    serializer_class = serializers.ProductDetailSerializer

    def get_queryset(self):
        return ProductVariant.objects.all()


class ProductListView(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    pagination_class = BaseProductsPagination

    def get_queryset(self):
        product_media = models.ProductMedia.objects.filter(
            type=choices.ProductMediaTypes.IMAGE,
            product_id=OuterRef('product_id')
        ).values('media_file')[:1]
        return ProductVariant.objects.all().annotate(
            product_media=Subquery(product_media)
        )

class SecureView(GenericAPIView):
    def get(self, request):
        return Response({"data": "secure"})
