from decimal import Decimal
from urllib.parse import parse_qsl

from django.conf import settings
from django.db.models import Min, OuterRef, Subquery
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from dataclasses import dataclass, asdict
from channel.models import Channel
from product import models
from product.models import ProductVariant


@dataclass
class PriceList:
    product_variant_id: int
    quantity: int
    unit_price: Decimal
    price: Decimal


@dataclass
class ResponseData:
    price_list: list
    total_sum: int
    currency: str


class CheckoutService:
    def __init__(self, *, request: Request):
        self.request = request

    def check_broken_variants(self, broken_variants: list):
        if broken_variants:
            raise ValidationError({'broken_variants': broken_variants})

    def from_list_of_dicts_get_key_values(self, key: str, list_of_dicts: list[dict]):
        return [d[key] for d in list_of_dicts]

    def from_channel_cookie_get_model(self):
        channel_model = models.Channel.objects.get(id=self.request.channel.id)
        return channel_model

    def form_price_list(self, product_variant_id: int, quantity: int, unit_price: Decimal):
        return asdict(
            PriceList(
                product_variant_id=product_variant_id,
                quantity=quantity,
                unit_price=unit_price,
                price=unit_price * quantity
            )
        )

    def form_response(self, price_list: list, total_sum: int, currency: str):
        return Response(asdict(
            ResponseData(
                price_list=price_list,
                total_sum=total_sum,
                currency=currency,
            )
        ))

    def form_checkout_data(self, serializer_data: list[dict]):
        prices = []
        total_price = 0
        broken_variants = []
        for unit in serializer_data:
            try:
                product = ProductVariant.objects.get(
                    id=unit['product_variant_id']
                )
            except ProductVariant.DoesNotExist:
                broken_variants.append(unit)
                continue

            channel_listing = product.channel_listings.get(channel_id=self.request.channel.id)
            data = self.form_price_list(
                product_variant_id=product.id,
                quantity=unit['quantity'],
                unit_price=channel_listing.cost_price
            )
            total_price += data['price']
            prices.append(data)
        self.check_broken_variants(broken_variants=broken_variants)
        channel_model = self.from_channel_cookie_get_model()
        return self.form_response(price_list=prices, total_sum=total_price, currency=channel_model.currency_code)


class ProductService:
    @staticmethod
    def decode_cookie(cookie: str) -> dict:
        return dict(parse_qsl(cookie))

    @staticmethod
    def is_channel_exists(channel_id: int) -> Response:
        return Channel.objects.filter(id=channel_id).exists()

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
        channel_id = request.channel.id
        channel = Channel.objects.filter(id=channel_id)
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
        return ProductVariant.objects.filter(
            id__in=[i[0] for i in list(serializer_input.values_list('product_variant'))]
        )

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
        variants = models.ProductVariant.objects.filter(channel_listings__in=product_variant).order_by('created')
        return [settings.MEDIA_URL + i[0] for i in variants.values_list('media__media_file')]
