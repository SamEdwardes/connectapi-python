from dataclasses import dataclass, field
from typing import Optional

from .client import Client
from .content import ContentEndpoint


@dataclass
class Api:
    client: Client = field(default_factory=Client)
    content: ContentEndpoint = field(init=False)

    """Create an interface for calling the Connect API.

    The `Api` class provides the primary interface for calling the Connect API.

    Params
    ------
    client: Client
        An instance of the Client class.

    Methods
    -------
    content: model.Content
        Exposes the `Content` class for querying `content` api endpoints.
    
    """    

    def __post_init__(self):
        print("Initiating client")
        self.content = ContentEndpoint(self.client)
