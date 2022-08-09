from rest_framework import serializers

from actions import choices
from api.v1.actions.services import ActionsService


class AssessmentSerializer(serializers.Serializer):
    like_type = serializers.ChoiceField(choices=choices.LikeTypeChoice.choices)
    object_id = serializers.IntegerField()
    vote = serializers.ChoiceField(choices=choices.LikeChoice.choices)

    def save(self, **kwargs):
        user = self.context['request'].user
        vote: int = self.validated_data["vote"]
        like_type: str = self.validated_data["like_type"]
        object_id: int = self.validated_data["object_id"]
        obj = ActionsService.get_like_object(like_type, object_id)
        if like := ActionsService.get_like(user, obj, object_id):
            if like.vote == vote:
                like.delete()
            else:
                like.vote = vote
                like.save(update_fields=["vote"])
        else:
            # Like.objects.create(user=user, content_type=, object_id=, vote=)
            obj.votes.create(user=user, vote=vote)

        return_data = {
            "likes_count": obj.likes()["count"],
            "dislike_count": obj.dislikes()["count"],
        }
        return return_data
