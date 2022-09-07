from rest_framework import serializers

from actions import choices
from actions.models import Like
from api.v1.actions.services import ActionsService
from django.contrib.auth import get_user_model

User = get_user_model()


class AssessmentSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    vote = serializers.ChoiceField(choices=choices.LikeChoice.choices)

    def save(self, **kwargs):
        user = self.context['request'].remote_user.id
        # vote: int = self.validated_data["vote"]
        product: int = self.validated_data["product"]
        obj = ActionsService.get_like_object(product)
        # if like := ActionsService.get_like(user, product):
        #     # if like.vote == vote:
        #     #     like.delete()
        #     # else:
        #     #     like.vote = vote
        #     #     like.save(update_fields=["vote"])
        # else:
        Like.objects.create(user_id=user, product_id=product)
        # obj.votes.create(user_id=user, vote=vote)

        # return_data = {
        #     "current_vote": obj.current_vote()["count"],
        # }
        return {"hello": "world"}
