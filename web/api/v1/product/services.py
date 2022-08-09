from urllib.parse import parse_qsl

from django.db.models import Min, OuterRef, Subquery
from rest_framework.request import Request
from rest_framework.response import Response

from channel.models import Channel
from product import models
from django.conf import settings


class ProductService:
    @staticmethod
    def decode_cookie(cookie: str) -> dict:
        return dict(parse_qsl(cookie))

    @staticmethod
    def is_channel_exists(channel_cookie: dict) -> Response:
        return Channel.objects.filter(**channel_cookie).exists()

    @staticmethod
    def get_full_price_of_product(obj, request: Request):
        if request.query_params.get('price_from') and request.query_params.get('price_to'):
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
                cost_price__gte=request.query_params.get('price_from'),
                cost_price__lte=request.query_params.get('price_to')
            ).aggregate(Min('cost_price'))
        elif request.query_params.get('price_from'):
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
                cost_price__gte=request.query_params.get('price_from')
            ).aggregate(Min('cost_price'))
        elif request.query_params.get('price_to'):
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
                cost_price__lte=request.query_params.get('price_to')
            ).aggregate(Min('cost_price'))
        else:
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
            ).aggregate(Min('cost_price'))
        return variants_channel_listings.get('cost_price__min')

    @staticmethod
    def get_media_of_product(obj, request: Request):
        if request.query_params.get('price_from') and request.query_params.get('price_to'):
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
                cost_price__gte=request.query_params.get('price_from'),
                cost_price__lte=request.query_params.get('price_to')
            ).aggregate(Min('cost_price'))
        elif request.query_params.get('price_from'):
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
                cost_price__gte=request.query_params.get('price_from')
            ).aggregate(Min('cost_price'))
        elif request.query_params.get('price_to'):
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
                cost_price__lte=request.query_params.get('price_to')
            ).aggregate(Min('cost_price'))
        else:
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
            ).aggregate(Min('cost_price'))
        media_variants = models.ProductVariantChannelListing.objects.get(
            product_variant__in=obj.variants.all(),
            cost_price=variants_channel_listings.get('cost_price__min')
        )
        return settings.MEDIA_URL + str(media_variants.product_variant.media.all().first().media_file)

    @staticmethod
    def get_variants_count(obj, request: Request):
        if request.query_params.get('price_from') and request.query_params.get('price_to'):
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
                cost_price__gte=request.query_params.get('price_from'),
                cost_price__lte=request.query_params.get('price_to')
            )
        elif request.query_params.get('price_from'):
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
                cost_price__gte=request.query_params.get('price_from')
            )
        elif request.query_params.get('price_to'):
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all(),
                cost_price__lte=request.query_params.get('price_to')
            )
        else:
            variants_channel_listings = models.ProductVariantChannelListing.objects.filter(
                product_variant__in=obj.variants.all()
            )

        variant = models.ProductVariant.objects.filter(channel_listings__in=variants_channel_listings,
                                                       channel_listings__visible_in_listings=True)
        return variant.count()

    @staticmethod
    def get_variants(obj, request: Request):
        channel = Channel.objects.filter(**request.COOKIES)
        if request.query_params.get('price_from') and request.query_params.get('price_to'):
            product_variant = models.ProductVariantChannelListing.objects.filter(
                channel__in=channel,
                visible_in_listings=True,
                product_variant__product=obj,
                cost_price__gte=request.query_params.get('price_from'),
                cost_price__lte=request.query_params.get('price_to')
            )
        elif request.query_params.get('price_from'):
            product_variant = models.ProductVariantChannelListing.objects.filter(
                channel__in=channel,
                visible_in_listings=True,
                product_variant__product=obj,
                cost_price__gte=request.query_params.get('price_from')
            )
        elif request.query_params.get('price_to'):
            product_variant = models.ProductVariantChannelListing.objects.filter(
                channel__in=channel,
                visible_in_listings=True,
                product_variant__product=obj,
                cost_price__lte=request.query_params.get('price_to')
            )
        else:
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
        return serializer_input

    @staticmethod
    def get_media_for_variants(obj, request: Request):
        if request.query_params.get('price_from') and request.query_params.get('price_to'):
            product_variant = models.ProductVariantChannelListing.objects.filter(
                product_variant__product=obj,
                cost_price__gte=request.query_params.get('price_from'),
                cost_price__lte=request.query_params.get('price_to')
            )
        elif request.query_params.get('price_from'):
            product_variant = models.ProductVariantChannelListing.objects.filter(
                product_variant__product=obj,
                cost_price__gte=request.query_params.get('price_from')
            )
        elif request.query_params.get('price_to'):
            product_variant = models.ProductVariantChannelListing.objects.filter(
                product_variant__product=obj,
                cost_price__lte=request.query_params.get('price_to')
            )
        else:
            product_variant = models.ProductVariantChannelListing.objects.filter(
                product_variant__product=obj
            )
        variants = models.ProductVariant.objects.filter(channel_listings__in=product_variant)
        return [settings.MEDIA_URL + i[0] for i in variants.values_list('media__media_file')]
