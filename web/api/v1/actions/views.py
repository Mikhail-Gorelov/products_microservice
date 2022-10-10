from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from actions.models import Like
from . import serializers
from .pagination import LikeNumberPagination


class AssessmentView(GenericAPIView):
    serializer_class = serializers.AssessmentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)


class AssessmentShowView(ListAPIView):
    serializer_class = serializers.AssessmentShowSerializer
    pagination_class = LikeNumberPagination

    def get_queryset(self):
        return Like.objects.filter(user_id=self.request.remote_user.id)
