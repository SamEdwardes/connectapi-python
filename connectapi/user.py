from __future__ import annotations

import datetime as dt
from typing import List

from pydantic import BaseModel

import connectapi

from .client import Client


class _UserBase(BaseModel):
    guid: str
    email: str
    username: str
    first_name: str
    last_name: str
    user_role: str
    created_time: dt.datetime
    updated_time: dt.datetime
    active_time: dt.datetime
    confirmed: bool
    locked: bool



class User(_UserBase):
    client: Client

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def whoami(cls, client: Client) -> User:
        with client() as _client:
            r = _client.get("/user")
        r.raise_for_status()
        return User(client=client, **r.json())

    def get_my_content(self) -> List[connectapi.content.Content]:
        with self.client() as _client:
            my_guid = _UserBase(**_client.get("/user").json()).guid
            r = _client.get(f"/content", params={"owner_guid": my_guid})
        r.raise_for_status()
        return [connectapi.content.Content(client=self.client, **i) for i in r.json()]
