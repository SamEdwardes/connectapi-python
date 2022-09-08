import httpx
from .config import Settings
from pydantic import BaseModel
from typing import Optional, List, Any

from rich import print, inspect

from .client import Client

class Content(BaseModel):
    guid: str
    name: str
    title: str
    description: str
    connection_timeout: Optional[int]


class ContentResponse(Content):
    response: Any


class ContentList(BaseModel):
    contents: List[Content]


class ContentListResponse(ContentList):
    response: Any


def get_content(
    owner_guid: Optional[str] = None,
    name: Optional[str] = None,
    client: Client = Client()
):
    class Params(BaseModel):
        owner_guid: Optional[str] = None
        name: Optional[str] = None

    params = Params(owner_guid=owner_guid, name=name)

    with client.create_client() as api:
        r = api.get(
            url="/content",
            params=params.dict(exclude_none=True)
        )
    
    return ContentListResponse(
        contents=[Content(**i) for i in r.json()],
        response=r
    )


def get_details(
    guid: str,
    client: Client = Client()
):
    with client.create_client() as api:
        r = api.get(url=f"content/{guid}")

    return ContentResponse(
        response=r,
        **r.json()
    )