from typing import Union, Optional

from product.models import Product
from actions.models import Like
from actions import choices
from django.contrib.contenttypes.models import ContentType
from main.models import UserType


class ActionsService:
    @staticmethod
    def get_like_object(object_id: int) -> Union[Product]:
        return Product.objects.get(id=object_id)

    @staticmethod
    def get_content_object(model_object: Union[Product]) -> ContentType:
        return ContentType.objects.get_for_model(model_object)

    @staticmethod
    def get_like(user: UserType, product_id: int) -> Optional[Like]:
        try:
            return Like.objects.get(user__id=user, product__id=product_id)
        except Like.DoesNotExist:
            return None
