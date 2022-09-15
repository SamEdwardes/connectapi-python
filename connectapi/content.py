from __future__ import annotations

import datetime as dt
from typing import List, Optional, Union

from pydantic import BaseModel, Field
from rich import inspect, print

from ._utils import remove_none_from_dict
from .client import Client


class ContentBase(BaseModel):
    guid: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    access_type: Optional[str] = None
    connection_timeout: Optional[int] = None
    read_timeout: Optional[int] = None
    init_timeout: Optional[int] = None
    idle_timeout: Optional[int] = None
    max_processes: Optional[int] = None
    min_processes: Optional[int] = None
    max_conns_per_process: Optional[int] = None
    load_factor: Optional[float] = None
    created_time: Optional[dt.datetime] = None
    last_deployed_time: Optional[dt.datetime] = None
    bundle_id: Optional[str] = None
    app_mode: Optional[str] = None
    content_category: Optional[str] = None
    parameterized: Optional[bool] = None
    cluster_name: Optional[str] = None
    image_name: Optional[str] = None
    r_version: Optional[str] = None
    py_version: Optional[str] = None
    quarto_version: Optional[str] = None
    run_as: Optional[str] = None
    run_as_current_user: bool = False
    owner_guid: Optional[str] = None
    content_url: Optional[str] = None
    dashboard_url: Optional[str] = None
    role: Optional[str] = None
    id: Optional[str] = None


class Content(ContentBase):
    """Manage content on Connect.

    The `Content` class is a module for managing all Content on Posit Connect.
    With the `Content` module you can:

    - Get information about existing content.
    - Edit the meta for existing content.
    - Deploy new content.

    Parameters
    ----------
    client: Client
    guid: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    access_type: Optional[str] = None
    connection_timeout: Optional[int] = None
    read_timeout: Optional[int] = None
    init_timeout: Optional[int] = None
    idle_timeout: Optional[int] = None
    max_processes: Optional[int] = None
    min_processes: Optional[int] = None
    max_conns_per_process: Optional[int] = None
    load_factor: Optional[float] = None
    created_time: Optional[dt.datetime] = None
    last_deployed_time: Optional[dt.datetime] = None
    bundle_id: Optional[str] = None
    app_mode: Optional[str] = None
    content_category: Optional[str] = None
    parameterized: Optional[bool] = None
    cluster_name: Optional[str] = None
    image_name: Optional[str] = None
    r_version: Optional[str] = None
    py_version: Optional[str] = None
    quarto_version: Optional[str] = None
    run_as: Optional[str] = None
    run_as_current_user: bool = False
    owner_guid: Optional[str] = None
    content_url: Optional[str] = None
    dashboard_url: Optional[str] = None
    role: Optional[str] = None
    id: Optional[str] = None

    See Also
    --------
    Content.get : Get existing content.
    Content.get_one : Get a specific piece of based on the guid.
    Content.create : Create a new piece of content.

    Examples
    --------
    Get all the content for a specific user.
    
    >>> from connectapi import Client, Content
    >>> client = Client()
    >>> contents = Content.get(client, owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")

    Get one specific piece of content.

    >>> from connectapi import Client, Content
    >>> client = Client()
    >>> content = Content.get_one(client, content_guid="241fe2cd-6eba-4a79-9aa3-6e6fe28c5714")
    """    
    client: Client

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def create(
        cls,
        client: Client,
        title: str,
        description: Optional[str] = None,
        name: Optional[str] = None,
        access_type: Optional[str] = 'acl',
        connection_timeout: Optional[int] = None,
        read_timeout: Optional[int] = None,
        init_timeout: Optional[int] = None,
        idle_timeout: Optional[int] = None,
        max_processes: Optional[int] = None,
        min_processes: Optional[int] = None,
        max_conns_per_process: Optional[int] = None,
        load_factor: Optional[float] = None,
        run_as: Optional[str] = None,
        run_as_current_user: bool = False
    ) -> Content:
        with client() as _client:
            content = ContentBase(
                title=title,
                description=description,
                name=name,
                access_type=access_type,
                connection_timeout=connection_timeout,
                read_timeout=read_timeout,
                init_timeout=init_timeout,
                idle_timeout=idle_timeout,
                max_processes=max_processes,
                min_processes=min_processes,
                max_conns_per_process=max_conns_per_process,
                load_factor=load_factor,
                run_as=run_as,
                run_as_current_user=run_as_current_user,
            )
            data = content.json(exclude_none=True)
            r = _client.post(url="/content", data=data)

        r.raise_for_status()
        return cls(
            client=client,
            **r.json()
        )
    
    @classmethod
    def get(
        cls, 
        client: Client, 
        owner_guid: Optional[str] = None,
    ) -> List[Content]:
        with client() as _client:
            params = remove_none_from_dict({"owner_guid": owner_guid})
            r = _client.get("/content/", params=params)
        r.raise_for_status()
        return [Content(client=client, **i) for i in r.json()]
    
    @classmethod
    def get_one(
        cls, 
        client: Client, 
        content_guid: str,
    ) -> Content:
        with client() as _client:
            r = _client.get(f"/content/{content_guid}")
        r.raise_for_status()
        return Content(client=client, **r.json())


# class ContentEndpoint:
#     """Get information related to your content deployed on Connect.

#     The ContentEndpoint class mirrors the endpoints described in 
#     https://docs.rstudio.com/connect/api/#tag--Content.

#     Params
#     ------
#     client: httpx.Client
#         An httpx.Client object.
#     """
#     def __init__(self, client: httpx.Client):
#         self.client = client

#     def list_items(
#         self, owner_guid: Optional[str] = None, name: Optional[str] = None
#     ) -> List[Content]:
#         """List all content items visible to the requesting user.

#         Authenticated access from a user is required. If an "administrator" role 
#         is used, then all content items will be returned regardless of the 
#         visibility to the requesting user.

#         Information about the target environment is populated for users with 
#         "publisher" and "administrator" role; it is suppressed for viewers.

#         See the official API docs for more details:
#         https://docs.rstudio.com/connect/api/#get-/v1/content.

#         Parameters
#         ----------
#         owner_guid : Optional[str], optional
#             The unique identifier of the user who owns the content. By default None
#         name : Optional[str], 
#             The content name specified when the content was created. Content 
#             names are unique within the owning user's account, so a request that 
#             specifies a non-empty name and owner_guid will return at most one 
#             content item.

#         Returns
#         -------
#         List[Content]
#             A list of Content objects.
#         """        
#         class Params(BaseModel):
#             owner_guid: Optional[str] = None
#             name: Optional[str] = None

#         with self.client as client:
#             params = Params(owner_guid=owner_guid, name=name)
#             r = client.get(url="/content", params=params.dict(exclude_none=True))

#         r.raise_for_status()
#         return [Content(**i) for i in r.json()]

#     def create_item(
#         self,
#         name: str,
#         title: str,
#         description: str,
#         access_type: str,
#         connection_timeout: int,
#         read_timeout: int,
#         init_timeout: int,
#         idle_timeout: int,
#         max_processes: int,
#         min_processes: int,
#         max_conns_per_process: int,
#         load_factor: float,
#         run_as: str,
#         run_as_current_user: str
#     ):
#         class Data(BaseModel):
#             name: str
#             title: str
#             description: str
#             access_type: str
#             connection_timeout: int
#             read_timeout: int
#             init_timeout: int
#             idle_timeout: int
#             max_processes: int
#             min_processes: int
#             max_conns_per_process: int
#             load_factor: float
#             run_as: str
#             run_as_current_user: str

#         with self.client as client:
#             data = Data(
#                 name=name,
#                 title=title,
#                 description=description,
#                 access_type=access_type,
#                 connection_timeout=connection_timeout,
#                 read_timeout=read_timeout,
#                 init_timeout=init_timeout,
#                 idle_timeout=idle_timeout,
#                 max_processes=max_processes,
#                 min_processes=min_processes,
#                 max_conns_per_process=max_conns_per_process,
#                 load_factor=load_factor,
#                 run_as=run_as,
#                 run_as_current_user=run_as_current_user
#             )
#             r = client.post(url="/content", data=data.dict(exclude_none=True))

#         r.raise_for_status()
#         return r
    
#     def get_details(self, guid: str) -> Content:
#         """_summary_

#         Parameters
#         ----------
#         guid : str
#             _description_

#         See the official API docs for more details: 
#         https://docs.rstudio.com/connect/api/#get-/v1/content/%7Bguid%7D

#         Returns
#         -------
#         Content
#             _description_
#         """
#         with self.client as client:
#             r = client.get(url=f"/content/{guid}")
#         r.raise_for_status()
#         return Content(**r.json())

