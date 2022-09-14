import datetime as dt
from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel
from rich import inspect, print

from .client import Client


class Content(BaseModel):
    guid: str
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    access_type: str
    connection_timeout: Optional[int] = None
    read_timeout: Optional[int] = None
    init_timeout: Optional[int] = None
    idle_timeout: Optional[int] = None
    max_processes: Optional[int] = None
    min_processes: Optional[int] = None
    max_conns_per_process: Optional[int] = None
    load_factor: Optional[float] = None
    created_time: dt.datetime
    last_deployed_time: dt.datetime
    bundle_id: str
    app_mode: str
    content_category: str
    parameterized: Optional[bool] = None
    cluster_name: Optional[str] = None
    image_name: Optional[str] = None
    r_version: Optional[str] = None
    py_version: Optional[str] = None
    quarto_version: Optional[str] = None
    run_as: Optional[str] = None
    run_as_current_user: bool
    owner_guid: str
    content_url: str
    dashboard_url: str
    role: Optional[str] = None
    id: Optional[str] = None


@dataclass
class ContentEndpoint:
    """ Get information related to your content deployed on Connect.

    The ContentEndpoint class mirrors the endpoints described in 
    https://docs.rstudio.com/connect/api/#tag--Content.
    """    
    client: Client

    def list_items(
        self, owner_guid: Optional[str] = None, name: Optional[str] = None
    ) -> List[Content]:
        """_summary_

        Parameters
        ----------
        owner_guid : Optional[str], optional
            _description_, by default None
        name : Optional[str], optional
            _description_, by default None

        Returns
        -------
        List[Content]
            _description_
        """        
        class Params(BaseModel):
            owner_guid: Optional[str] = None
            name: Optional[str] = None

        with self.client.create_client() as api:
            params = Params(owner_guid=owner_guid, name=name)
            r = api.get(url="/content", params=params.dict(exclude_none=True))

        r.raise_for_status()
        return [Content(**i) for i in r.json()]
    
    def get_details(self, guid: str) -> Content:
        """_summary_

        Parameters
        ----------
        guid : str
            _description_

        Returns
        -------
        Content
            _description_
        """
        with self.client.create_client() as api:
            r = api.get(url=f"/content/{guid}")
        r.raise_for_status()
        return Content(**r.json())

