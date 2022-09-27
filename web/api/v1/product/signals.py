from django import dispatch
from django.db.models.signals import post_save, pre_save

from src.celery import app
from django.dispatch import receiver

from product.models import ProductVariantChannelListing


@receiver(post_save, sender=ProductVariantChannelListing)
def test_signal(instance: ProductVariantChannelListing, **kwargs):
    print(instance.price, instance.cost_price, kwargs)
    app.send_task(name='update_price', exchange='generic')
    return
