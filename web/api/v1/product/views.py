from decimal import Decimal

from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import CharField, Q

from product.pagination import BaseProductsPagination
from product import models, choices
from django.db.models import Sum, Subquery, OuterRef, Count
from channel.models import Channel
from product.models import Category, Product, ProductVariant, ProductVariantChannelListing
from . import serializers
from .filters import ProductsFilter
from .services import ProductService


class HotProductsView(ListAPIView):
    permission_classes = (AllowAny,)
    filterset_class = ProductsFilter
    pagination_class = BaseProductsPagination
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        if not ProductService.is_channel_exists(self.channel_cookie):
            return None
        channel = Channel.objects.filter(**self.channel_cookie)
        price_from = self.request.query_params.get('price_from', 0)
        price_to = self.request.query_params.get('price_to', 999999.99)
        product_variant = models.ProductVariantChannelListing.objects.filter(
            cost_price__gte=Decimal(str(price_from)),
            cost_price__lte=Decimal(str(price_to)),
            channel__in=channel,
            visible_in_listings=True
        )
        basic_filtration = models.Product.objects.filter(
            variants__channel_listings__in=product_variant,
            is_bestseller=True,
        ).distinct()
        return basic_filtration

    def list(self, request, *args, **kwargs):
        self.channel_cookie = {k: v[0] for k, v in dict(request.data).items()}
        return super().list(request, *args, **kwargs)


class HotProductsDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ProductDetailUnitSerializer

    def get_queryset(self):
        return Product.objects.filter(is_bestseller=True)

    def retrieve(self, request, *args, **kwargs):
        # TODO: сделать ещё фильтрацию по регионам, чтобы всегда был get на один листинг (один вариант - один листинг)
        self.channel_cookie = {k: v[0] for k, v in dict(request.data).items()}
        if not ProductService.is_channel_exists(self.channel_cookie):
            return None
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoriesView(GenericAPIView):
    def get(self, request):
        return Response(Category.dump_bulk())


class ProductDetailView(RetrieveAPIView):
    serializer_class = serializers.ProductDetailUnitSerializer

    def get_queryset(self):
        return Product.objects.all()


class ProductListView(ListAPIView):
    serializer_class = serializers.ProductDetailUnitSerializer
    pagination_class = BaseProductsPagination

    def get_queryset(self):
        return Product.objects.all()


class SecureView(GenericAPIView):
    def get(self, request):
        return Response({"data": "secure"})


class ProductsView(GenericAPIView):
    serializer_class = serializers.ProductsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_media = models.ProductMedia.objects.filter(
            type=choices.ProductMediaTypes.IMAGE,
            product_id=OuterRef('product_id'),
        ).values('media_file')[:1]
        queryset = ProductVariant.objects.filter(id__in=serializer.data.get('products')).annotate(
            product_media=Subquery(product_media),
        )
        list_serializer = serializers.ProductListSerializer(queryset, many=True)
        return Response(list_serializer.data)
