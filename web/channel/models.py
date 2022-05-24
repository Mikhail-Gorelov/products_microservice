from django.db import models
from django_countries.fields import CountryField

class Channel(models.Model):
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)
    currency_code = models.CharField(max_length=20)
    country = CountryField()

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'

    def __str__(self):
        return self.slug
