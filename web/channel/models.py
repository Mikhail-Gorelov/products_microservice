from django.db import models
from unidecode import unidecode
from django.utils.text import slugify
from django_countries.fields import CountryField


class Channel(models.Model):
    name = models.CharField(max_length=250, unique=True)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    currency_code = models.CharField(max_length=20)
    country = CountryField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'

    def __str__(self):
        return self.slug
