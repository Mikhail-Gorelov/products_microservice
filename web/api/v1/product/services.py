from urllib.parse import parse_qsl
from rest_framework.response import Response

from channel.models import Channel


class ProductService:
    @staticmethod
    def decode_cookie(cookie: str) -> dict:
        return dict(parse_qsl(cookie))

    @staticmethod
    def is_channel_exists(channel_cookie: dict) -> Response:
        return Channel.objects.filter(**channel_cookie).exists()
