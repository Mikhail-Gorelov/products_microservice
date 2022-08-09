from typing import Union, Optional

from product.models import Product
from actions.models import Like
from actions import choices
from django.contrib.contenttypes.models import ContentType
from main.models import UserType


class ActionsService:
    @staticmethod
    def get_like_object(like_type: str, object_id: int) -> Union[Product]:
        if like_type == choices.LikeTypeChoice.PRODUCT:
            return Product.objects.get(id=object_id)

    @staticmethod
    def get_content_object(model_object: Union[Product]) -> ContentType:
        return ContentType.objects.get_for_model(model_object)

    @staticmethod
    def get_like(user: UserType, obj: Union[Product], object_id: int) -> Optional[Like]:
        content_type = ActionsService.get_content_object(obj)
        try:
            return Like.objects.get(user=user, content_type=content_type, object_id=object_id)
        except Like.DoesNotExist:
            return None
