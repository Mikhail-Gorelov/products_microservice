from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import serializers


class AssessmentView(GenericAPIView):
    serializer_class = serializers.AssessmentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)
