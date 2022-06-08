from django.db import models
from treebeard.mp_tree import MP_Node
from channel.models import Channel
from unidecode import unidecode
from django.template import defaultfilters
from django.utils.text import slugify
from . import choices


class ProductType(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    kind = models.CharField(max_length=32, choices=choices.ProductTypeKind.CHOICES)
    has_variants = models.BooleanField(default=True)
    is_shipping_required = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)
    category = models.ForeignKey(
        "Category", related_name="product_type", on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'ProductType'
        verbose_name_plural = 'ProductTypes'


class Category(MP_Node):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.CharField(max_length=300)
    background_image = models.ImageField(
        upload_to="category-images", blank=True, null=True
    )

    node_order_by = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'Category: {}'.format(self.name)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_type = models.ForeignKey(
        ProductType, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True,
    )
    default_variant = models.OneToOneField(
        "ProductVariant",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="default_variant",
    )
    rating = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductVariant(models.Model):
    name = models.CharField(max_length=255, blank=True)
    product = models.ForeignKey(
        Product, related_name="variants", on_delete=models.CASCADE
    )
    media = models.ManyToManyField("ProductMedia", through="VariantMedia")
    track_inventory = models.BooleanField(default=True)
    is_preorder = models.BooleanField(default=False)
    preorder_end_date = models.DateTimeField(null=True, blank=True)
    preorder_threshold = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ProductVariant'
        verbose_name_plural = 'ProductVariants'


class ProductMedia(models.Model):
    product = models.ForeignKey(
        Product, related_name="media", on_delete=models.SET_NULL, null=True, blank=True
    )
    media_file = models.FileField(
        upload_to="products", blank=True, null=True
    )
    type = models.CharField(
        max_length=32,
        choices=choices.ProductMediaTypes.CHOICES,
        default=choices.ProductMediaTypes.IMAGE,
    )
    external_url = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'ProductMedia'
        verbose_name_plural = 'ProductMedias'


class VariantMedia(models.Model):
    variant = models.ForeignKey(
        ProductVariant, related_name="variant_media", on_delete=models.CASCADE
    )
    media = models.ForeignKey(
        ProductMedia, related_name="variant_media", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("variant", "media")


class ProductVariantChannelListing(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant,
        null=False,
        blank=False,
        related_name="channel_listings",
        on_delete=models.CASCADE,
    )
    channel = models.ForeignKey(
        Channel,
        null=False,
        blank=False,
        related_name="variant_listings",
        on_delete=models.CASCADE,
    )
    visible_in_listings = models.BooleanField(default=True)
    available_to_purchase = models.BooleanField(default=True)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )
    cost_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )
    is_bestseller = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        unique_together = [["product_variant", "channel"]]
        ordering = ("pk",)
        verbose_name = 'ProductVariantChannelListing'
        verbose_name_plural = 'ProductVariantChannelListings'
