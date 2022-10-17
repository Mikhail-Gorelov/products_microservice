import json
from decimal import Decimal

from django.db.models import Subquery, OuterRef, Sum, Case, When
from oauthlib.common import urldecode
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from channel.models import Channel
from product import models, choices
from product.models import Category, Product, ProductVariant
from product.pagination import BaseProductsPagination
from . import serializers
from .filters import ProductsFilter, ProductsSearchFilter
from .services import ProductService


class ProductsListView(ListAPIView):
    permission_classes = (AllowAny,)
    filterset_class = ProductsFilter
    pagination_class = BaseProductsPagination
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        channel_cookie = dict(urldecode(self.request.COOKIES.get('reg_country')))
        channel = Channel.objects.filter(**channel_cookie)
        return Product.objects.filter(variants__channel_listings__channel__in=channel).distinct()


class ProductsDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ProductDetailUnitSerializer
    queryset = Product.objects.filter()

    def retrieve(self, request, *args, **kwargs):
        channel_cookie = dict(urldecode(self.request.COOKIES.get('reg_country')))
        if not ProductService.is_channel_exists(channel_cookie):
            return None
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoriesView(GenericAPIView):
    def get(self, request):
        return Response(Category.dump_bulk())


class CategoriesDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductsVariantView(RetrieveAPIView):
    serializer_class = serializers.ProductVariantDetailSerializer
    queryset = ProductVariant.objects.all()


class ProductListView(ListAPIView):
    serializer_class = serializers.ProductDetailUnitSerializer
    pagination_class = BaseProductsPagination
    queryset = Product.objects.all()


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


class ChannelListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ChannelSerializer
    queryset = Channel.objects.filter(is_active=True)


class SearchProductView(ListAPIView):
    permission_classes = (AllowAny,)
    filterset_class = ProductsSearchFilter
    serializer_class = serializers.ProductSearchSerializer

    def get_queryset(self):
        channel_cookie = dict(urldecode(self.request.COOKIES.get('reg_country')))
        channel = Channel.objects.filter(**channel_cookie)
        return Product.objects.filter(variants__channel_listings__channel__in=channel).distinct()


class TotalSumView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.TotalPositionsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        variants = models.ProductVariant.objects.filter(id__in=serializer.data.get('variant_ids'))
        id_s = list(variants.values_list('id', flat=True))
        values = list(variants.values_list('channel_listings__cost_price', flat=True))
        zip_iterator = dict(zip(id_s, values))
        return Response(zip_iterator)


class TotalWeightView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.TotalWeightSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        converted_list = json.loads(json.dumps(serializer.data))
        variant_ids = [d['variant_id'] for d in converted_list]
        quantity = [d['quantity'] for d in converted_list]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(variant_ids)])
        queryset = ProductVariant.objects.filter(
            pk__in=variant_ids
        ).order_by(preserved).values_list('weight', flat=True)
        product_variants = [Decimal('0') if v is None else v for v in queryset]
        multiplied_list = [a * b for a, b in zip(product_variants, quantity)]
        return Response({'total_weight': sum(multiplied_list)})
