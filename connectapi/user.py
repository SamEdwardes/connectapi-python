from pydantic import BaseModel
import datetime as dt
from .client import Client
# from .content import Content


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
    def whoami(cls, client: Client):
        with client() as _client:
            r = _client.get("/user")
        r.raise_for_status()
        return User(client=client, **r.json())

    # @classmethod
    # def get_my_content(cls, client: Client) -> Content:
    #     with client() as _client:
    #         my_guid = _UserBase(**_client.get("/user").json()).guid
    #         r = _client.get(f"/content", params={"owner_guid": my_guid})
    #     r.raise_for_status()
    #     return [Content(client=client, **i) for i in r.json()]
