from django.db import models
from django.contrib.auth import get_user_model
from actions.choices import LikeChoice
from product.models import Product

User = get_user_model()



class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_likes'
    )
    product = models.ForeignKey(Product, related_name="product_like", on_delete=models.CASCADE, null=True)
    vote = models.PositiveSmallIntegerField(choices=LikeChoice.choices, db_index=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
