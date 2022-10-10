from django.db.models.signals import post_save
from django.dispatch import receiver

from product.models import ProductVariantChannelListing
from src.celery import app


@receiver(post_save, sender=ProductVariantChannelListing)
def test_signal(instance: ProductVariantChannelListing, **kwargs):
    app.send_task(name='update_prices', kwargs={
        'id': instance.pk,
        'price': instance.price,
        'cost_price': instance.cost_price,
        'channel': {
            'id': instance.channel.pk,
            'is_active': instance.channel.is_active,
            'slug': instance.channel.slug,
            'currency_code': instance.channel.currency_code,
            'country': str(instance.channel.country),
        },
        'product_variant': {
            'id': instance.product_variant.pk,
        },
        'product': {
            'id': instance.product_variant.product.pk,
        },
    }, exchange='generic', routing_key='celery')
    return
