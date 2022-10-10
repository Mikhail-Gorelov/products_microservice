from django.contrib.auth import get_user_model
from rest_framework import serializers

from actions.models import Like
from api.v1.actions.services import ActionsService
from api.v1.product.serializers import ProductSerializer
from product.models import Product

User = get_user_model()


class AssessmentSerializer(serializers.Serializer):
    product = serializers.IntegerField()

    def save(self, **kwargs):
        user_id = self.context['request'].remote_user.id
        product: int = self.validated_data["product"]
        if not Product.objects.filter(id=product).exists():
            return {'is_liked': False}
        if like := ActionsService.get_like(user_id, product):
            like.delete()
            return {'is_liked': False}
        else:
            Like.objects.create(user_id=user_id, product_id=product)
            return {'is_liked': True}


class AssessmentShowSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data['product']

    class Meta:
        model = Like
        fields = ('product',)
