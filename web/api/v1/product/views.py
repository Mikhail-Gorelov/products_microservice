from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from product import models
from channel.models import Channel
from . import serializers
from microservice_request.permissions import HasApiKeyOrIsAuthenticated
from .services import ProductService


class HotProductsView(GenericAPIView):
    permission_classes = (HasApiKeyOrIsAuthenticated,)
    serializer_class = serializers.HotProductsSerializer

    def get_queryset(self):
        if ProductService.is_channel_exists(self.channel_cookie):
            channel = Channel.objects.get(**self.channel_cookie)
            return models.ProductVariantChannelListing.objects.filter(channel=channel,
                                                                  is_bestseller=True,
                                                                  visible_in_listings=True)
        else:
            return None

    def get(self, request):
        self.channel_cookie = {k: v[0] for k, v in dict(request.data).items()}
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
