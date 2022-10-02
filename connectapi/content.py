from __future__ import annotations

import datetime as dt
import time
import tarfile
from pathlib import Path
from typing import List, Optional, Set, Union
from uuid import uuid4
import sys

from pydantic import BaseModel, Field, validator
from rich import inspect, print
from rich.live import Live
from rich.prompt import Confirm

import connectapi

from ._console import console
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

    @validator('name')
    def name_must_contain_space(cls, v):
        if v is None:
            return uuid4()
        else:
            return v

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
    >>> contents = Content.get_many(client, owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")

    Get one specific piece of content.

    >>> from connectapi import Client, Content
    >>> client = Client()
    >>> content = Content.get_one(client, content_guid="241fe2cd-6eba-4a79-9aa3-6e6fe28c5714")
    """    
    client: Client
    editable_fields: Set[str] = {
        "name",
        "title",
        "description",
        "access_type",
        "owner_guid",
        "connection_timeout",
        "read_timeout",
        "init_timeout",
        "idle_timeout",
        "max_processes",
        "min_processes",
        "max_conns_per_process",
        "load_factor",
        "run_as",
        "run_as_current_user"
    }

    class Config:
        arbitrary_types_allowed = True

        
    def update(self):
        with self.client() as client:
            data = self.json(include=self.get_editable_fields(), exclude_none=True)
            r = client.patch(url=f"/content/{self.guid}", data=data)
        r.raise_for_status()
        # Update self with the response.
        for key, value in r.json().items():
            if key in self.dict():
                self.__setattr__(key, value)
        return self

    def delete(self, force=False) -> Content:
        if force == False:
            delete = Confirm.ask(
                f"[bold red]Are you sure you want to delete[/] [yellow italic]'{self.dict(include={'title', 'guid'})}[/][bold red]?",
                console=console
            )
        else:
            console.print(f"[bold red]Deleting[/] [yellow italic]'{self.dict(include={'title', 'guid'})}")
            delete = True
        if delete:
            with self.client() as client:
                r = client.delete(url=f"/content/{self.guid}")
            r.raise_for_status()
            console.print("Content successfully deleted.")
        else:
            console.print("Content NOT deleted.")

    def get_dashboard_view_url(self):
        return f"{self.client.connect_server}/connect/#/apps/{self.guid}"
    
    def get_solo_view_url(self):
        "https://colorado.rstudio.com/rsc/demo-quarto-colorado-report-r/"
        return f"{self.client.connect_server}/{self.guid}"

    @classmethod
    def get_editable_fields(cls) -> Set:
        return {
            "name",
            "title",
            "description",
            "access_type",
            "owner_guid",
            "connection_timeout",
            "read_timeout",
            "init_timeout",
            "idle_timeout",
            "max_processes",
            "min_processes",
            "max_conns_per_process",
            "load_factor",
            "run_as",
            "run_as_current_user"
        }


    @classmethod
    def create(
        cls,
        client: Client,
        directory: Optional[str] = None,
        title: Optional[str] = None,
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
        content_input = ContentBase(
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
        with client() as _client:
            console.rule("Creating new content")
            response_content = _client.post(
                url="/content", 
                content=content_input.json(exclude_none=True)
            )
            response_content.raise_for_status()
            content = cls(client=client, **response_content.json())
            print(f"[bold green]Content successfully created")
            print(content.dict(include={'guid', 'title'}))
            
            if directory:
                console.rule("Uploading bundle")
                bundle = Bundle(directory)
                bundle_data = bundle.bundle_path.read_bytes()
                response_bundle = _client.post(
                    f"/experimental/content/{content.guid}/upload",
                    data=bundle_data
                )
                response_bundle.raise_for_status()
                
                class BundleUploadResponse(BaseModel):
                    bundle_id: str
                    bundle_size: int

                bundle_upload_response = BundleUploadResponse(**response_bundle.json())

                console.rule("Deploying bundle")
                console.print(f"Deploying bundle '{bundle_upload_response.bundle_id}'")
                response_deploy = _client.post(
                    f"/experimental/content/{content.guid}/deploy",
                    data = bundle_upload_response.json(include={'bundle_id'})
                )
                task_id: str = response_deploy.json()["task_id"]
                response_deploy.raise_for_status()

                with console.status("Deploying..."):
                    logs = []
                    for i in range(20):
                        time.sleep(2)
                        task_response = _client.get(f"/tasks/{task_id}")
                        new_logs = task_response.json()["output"]
                        # if the logs have not changed do nothing.
                        if new_logs == logs:
                            continue
                        # trim the logs to only show new output.
                        logs = new_logs[len(logs):]
                        for i in logs:
                                console.print(f"[yan dim]{i}")
                        if task_response.json()['finished']:
                            console.log("[bold green]Content successfully deployed")
                            break


        console.rule("Deployment details")
        console.print("[bold green]New content created:")
        console.print(f"- Dashboard view url: {content.get_dashboard_view_url()}")
        console.print(f"- Solo view url: {content.get_solo_view_url()}")

        return content

    @classmethod
    def get_many(
        cls, 
        client: Client, 
        owner_guid: Optional[str] = None,
    ) -> List[Content]:
        with client() as _client:
            params = remove_none_from_dict({"owner_guid": owner_guid})
            r = _client.get("/content", params=params)
        r.raise_for_status()
        return [Content(client=client, **i) for i in r.json()]
    
    @classmethod
    def get_one(
        cls, 
        client: Client, 
        content_guid: str,
    ) -> Content:
        """Get a single piece of content based on the content's guid.

        Parameters
        ----------
        client : Client
            A connectapi Client object.
        content_guid : str
            The unique identifier for the content.

        Returns
        -------
        Content
            A connectapi Content object.
        """    
        with client() as _client:
            r = _client.get(f"/content/{content_guid}")
        r.raise_for_status()
        return Content(client=client, **r.json())
    
    @classmethod
    def get_my_content(cls, client: Client) -> List[Content]:
        """Get all of the content for the current user.

        Parameters
        ----------
        client : Client
            A connectapi Client object.

        Returns
        -------
        List[Content]
            A list of all content for the current user.
        """             
        with client() as _client:
            my_guid = connectapi.user._UserBase(**_client.get("/user").json()).guid
            r = _client.get(f"/content", params={"owner_guid": my_guid})
        r.raise_for_status()
        return [Content(client=client, **i) for i in r.json()]


class Bundle:
    directory: str
    bundle_path: Path

    def __init__(self,directory: str = "."):
        self.directory = directory
        path = Path(directory)
        if Path(path, "manifest.json").exists() == False:
            raise ValueError("No manifest.json file found")
        self.bundle_path = self._create_tarball(directory)
        
    def _create_tarball(self, directory: str) -> Path:
        path = Path(directory)
        r_files = list(path.glob('**/*.R'))
        unique_id = str(uuid4())
        # unique_id = "1"
        tarball_name = f"bundle-{unique_id}.tar.gz"
        bundle_path = Path(path, tarball_name)
        console.print(f"Adding files to tarball [italic]{bundle_path}")
        with tarfile.open(bundle_path, "w:gz") as tar:
            files_to_add = [path / "manifest.json"] + r_files
            for f in files_to_add :
                console.print(f"- {f}")
                tar.add(f, f.name)
        return bundle_path
