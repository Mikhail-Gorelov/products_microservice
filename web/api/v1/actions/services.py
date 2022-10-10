from typing import Union, Optional

from actions.models import Like
from product.models import Product


class ActionsService:
    @staticmethod
    def get_like_object(object_id: int) -> Union[Product]:
        return Product.objects.get(id=object_id)

    @staticmethod
    def get_like(user_id: int, product_id: int) -> Optional[Like]:
        try:
            return Like.objects.get(user_id=user_id, product__id=product_id)
        except Like.DoesNotExist:
            return None
