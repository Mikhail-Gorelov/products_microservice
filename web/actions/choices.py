from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class LikeChoice(IntegerChoices):
    LIKE = (1, _('Like'))
    DISLIKE = (0, _('Dislike'))


class LikeTypeChoice(TextChoices):
    PRODUCT = ("product", _("Product"))
