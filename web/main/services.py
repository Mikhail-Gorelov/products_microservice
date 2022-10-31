from dataclasses import dataclass
from typing import Optional


@dataclass
class RemoteUser:
    id: int
    session: Optional[str]


@dataclass
class ChannelCookie:
    id: int
    name: str
    slug: str
    currency_code: str
    country: str
