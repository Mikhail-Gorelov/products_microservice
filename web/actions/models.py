from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

from actions.choices import LikeChoice

User = get_user_model()

limit = models.Q(app_label='product', model='product')


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_likes'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    vote = models.PositiveSmallIntegerField(choices=LikeChoice.choices, db_index=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
