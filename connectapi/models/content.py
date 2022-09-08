import httpx
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional, List, Any
from ..client import Client


from rich import print, inspect


class Content(BaseModel):
    guid: str
    name: str
    title: str
    description: str
    connection_timeout: Optional[int]

    # guid: uuid 🆁
    # The unique identifier of this content item.

    # name: string
    # A simple, URL-friendly identifier. Allows alpha-numeric characters, hyphens ("-"), and underscores ("_").

    # title: string
    # Default: null
    # The title of this content.

    # description: string
    # A rich description of this content.

    # access_type: enum
    # Default: acl
    # Allowed:   all, logged_in, acl
    # Access type describes how this content manages its viewers. The value all is the most permissive; any visitor to RStudio Connect will be able to view this content. The value logged_in indicates that all RStudio Connect accounts may view the content. The acl value lets specifically enumerated users and groups view the content. Users configured as collaborators may always view content.

    # connection_timeout: int32
    # Default: null
    # Maximum number of seconds allowed without data sent or received across a client connection. A value of 0 means connections will never time-out (not recommended). When null, the default Scheduler.ConnectionTimeout is used. Applies only to content types that are executed on demand.

    # read_timeout: int32
    # Default: null
    # Maximum number of seconds allowed without data received from a client connection. A value of 0 means a lack of client (browser) interaction never causes the connection to close. When null, the default Scheduler.ReadTimeout is used. Applies only to content types that are executed on demand.

    # init_timeout: int32
    # Default: null
    # The maximum number of seconds allowed for an interactive application to start. RStudio Connect must be able to connect to a newly launched application before this threshold has elapsed. When null, the default Scheduler.InitTimeout is used. Applies only to content types that are executed on demand.

    # idle_timeout: int32
    # Default: null
    # The maximum number of seconds a worker process for an interactive application to remain alive after it goes idle (no active connections). When null, the default Scheduler.IdleTimeout is used. Applies only to content types that are executed on demand.

    # max_processes: int32
    # Default: null
    # Specifies the total number of concurrent processes allowed for a single interactive application. When null, the default Scheduler.MaxProcesses is used. Applies only to content types that are executed on demand.

    # min_processes: int32
    # Default: null
    # Specifies the minimum number of concurrent processes allowed for a single interactive application. When null, the default Scheduler.MinProcesses is used. Applies only to content types that are executed on demand.

    # max_conns_per_process: int32
    # Default: null
    # Specifies the maximum number of client connections allowed to an individual process. Incoming connections which will exceed this limit are routed to a new process or rejected. When null, the default Scheduler.MaxConnsPerProcess is used. Applies only to content types that are executed on demand.

    # load_factor: float
    # Default: null
    # Controls how aggressively new processes are spawned. When null, the default Scheduler.LoadFactor is used. Applies only to content types that are executed on demand.

    # created_time: date-time 🆁
    # The timestamp (RFC3339) indicating when this content was created.

    # last_deployed_time: date-time 🆁
    # The timestamp (RFC3339) indicating when this content last had a successful bundle deployment performed.

    # bundle_id: string 🆁
    # The identifier for the active deployment bundle. Automatically assigned upon the successful deployment of that bundle.

    # app_mode: enum 🆁
    # Allowed:   api, jupyter-static, python-api, python-bokeh, python-dash, python-streamlit, quarto-shiny, quarto-static, rmd-shiny, rmd-static, shiny, static, tensorflow-saved-model, unknown
    # The runtime model for this content. Has a value of unknown before data is deployed to this item. Automatically assigned upon the first successful bundle deployment.

    # Valid values are:

    # api - R code defining a Plumber API.
    # jupyter-static - A Jupyter Notebook.
    # python-api - Python code defining a WSGI API (such as Flask)
    # python-bokeh - Python code defining a Bokeh application.
    # python-dash - Python code defining a Dash application.
    # python-fastapi - Python code defining an ASGI API (such as FastAPI)
    # python-streamlit - Python code defining a Streamlit application.
    # quarto-shiny - A Quarto document with a Shiny runtime.
    # quarto-static - A Quarto document or site.
    # rmd-shiny - An R Markdown document with a Shiny runtime.
    # rmd-static - An R Markdown document or site.
    # shiny - R code defining a Shiny application.
    # static - Content deployed without source; often HTML and plots.
    # tensorflow-saved-model - A TensorFlow Model API.
    # unknown - No known runtime model.
    # content_category: string 🆁
    # Describes the specialization of the content runtime model. Automatically assigned upon the first successful bundle deployment.

    # The content_category field refines the type of content specified by app_mode. It is empty by default. The rsconnect R package may assign a value when analyzing your content and building its manifest and bundle. Plots (images created in the RStudio IDE and presented in the "Plots" pane) have an app_mode of static and receive a content_category of plot to distinguish them from other HTML documents. Pinned static data sets have an app_mode of static and a content_category of pin. Multi-document R Markdown sites have an app_mode of rmd-static and a content_category of site.

    # parameterized: boolean 🆁
    # True when R Markdown rendered content allows parameter configuration. Automatically assigned upon the first successful bundle deployment. Applies only to content with an app_mode of rmd-static.

    # cluster_name: string 🆁
    # The location where this content runs. Content running on the same server as Connect will have either a null value or the string "Local". Gives the name of the cluster when run external to the Connect host.

    # image_name: string 🆁
    # The location where content this content runs. Content running on the same server as Connect will have either a null value or the string "Local". References the name of the target image when content runs in a clustered environment such as Kubernetes.

    # r_version: string 🆁
    # The version of the R interpreter associated with this content. The value null represents that an R interpreter is not used by this content or that the client does not have sufficient rights to see this information or that the R package environment has not been successfully restored. Automatically assigned upon the successful deployment of a bundle.

    # py_version: string 🆁
    # The version of the Python interpreter associated with this content. The value null represents that a Python interpreter is not used by this content or that the client does not have sufficient rights to see this information or that the Python package environment has not been successfully restored. Automatically assigned upon the successful deployment of a bundle.

    # quarto_version: string 🆁
    # The version of Quarto associated with this content. The value null represents that Quarto is not used by this content or that the client does not have sufficient rights to see this information or that the content has not been successfully prepared for execution. Automatically assigned upon the successful deployment of a bundle.

    # run_as: string 🆁
    # Default: null
    # The UNIX user that executes this content. When null, the default Applications.RunAs is used. Applies only to executable content types - not static. Only administrators can change this value.

    # run_as_current_user: boolean 🆁
    # Default: false
    # Indicates that Connect should run processes for this content item under the unix account of the user who visits it. Connect must be configured with PAM authentication, and additionally configure Applications.RunAsCurrentUser = true and PAM.ForwardPassword = true. This setting only applies to application content types (Shiny, Dash, Streamlit, and Bokeh). Only administrators can change this value.

    # owner_guid: uuid
    # The unique identifier of the user who created this content item. Automatically assigned when the content is created.

    # content_url: string 🆁
    # The URL associated with this content. Computed from the associated vanity URL or GUID for this content.

    # dashboard_url: string 🆁
    # The URL within the Connect dashboard where this content can be configured. Computed from the GUID for this content.

    # role: enum 🆁
    # Allowed:   owner, editor, viewer, none
    # The relationship of the accessing user to this content. A value of owner is returned for the content owner. editor indicates a collaborator. The viewer value is given to users who are permitted to view the content. A none role is returned for administrators who cannot view the content but are permitted to view its configuration. Computed at the time of the request.

    # id: string 🆁
    # The internal numeric identifier of this content item.



@dataclass
class ContentApi:
    client: Client

    def get_details(self, guid: str) -> Content:
        with self.client.create_client() as api:
            r = api.get(url=f"content/{guid}")
        return Content(**r.json())

    def get_content(self, owner_guid: Optional[str] = None, name: Optional[str] = None) -> List[Content]:
        class Params(BaseModel):
            owner_guid: Optional[str] = None
            name: Optional[str] = None

        params = Params(owner_guid=owner_guid, name=name)

        with self.client.create_client() as api:
            r = api.get(
                url="/content",
                params=params.dict(exclude_none=True)
            )
        
        return [Content(**i) for i in r.json()]