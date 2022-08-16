from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()


class Like(models.Model):
    user_id = models.PositiveIntegerField()
    product = models.ForeignKey(Product, related_name="product_like", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'product'], name='Unique user like')
        ]
        ordering = ('-date',)
