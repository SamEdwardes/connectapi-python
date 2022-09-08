from dataclasses import dataclass, field
from .models.content import ContentApi
from .client import Client
from typing import Optional


@dataclass
class Api:
    client: Client = field(default_factory=Client)
    content: ContentApi = field(init=False)

    def __post_init__(self):
        self.content = ContentApi(self.client)

    def _call(self, url: str, params: Optional[dict] = None):
        with self.client.create_client() as client:
            r = client.get(url=url, params=params)
        return r


