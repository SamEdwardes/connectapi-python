import os
from typing import Optional
from pydantic import BaseSettings, validator

import httpx

from .content import ContentEndpoint


class Client(BaseSettings):
    connect_server: str
    connect_api_key: str
    api_endpoint: Optional[str]
    """Create a connection to the Connect server.
    Params
    ------
    connect_server: str | None
        The server endpoint. If `None` connectapi will look for an environment 
        variable `CONNECT_SERVER`. For example 'https://colorado.rstudio.com/rsc'.
        By default, `None`.
    connect_api_key: str | None
        The API key to connect to the Connect server. If `None` connectapi will
        look for an environment variable `CONNECT_API_KEY`. By default, `None`.
    api_endpoint: str | None
        By default connectapi will automatically determine the API endpoint based
        on the `connect_server`. For example if
        `connect_server='https://colorado.rstudio.com/rsc'` is used the
        `api_endpoint` will automatically be set to
        'https://colorado.rstudio.com/rsc/__api__/v1'. However, if you would like
        to override this behaviour your can manually specify the `api_endpoint`.
        For example 'https://colorado.rstudio.com/rsc/api/__api__/v1'. By default,
        `None`.
    Examples
    --------
    Create a client that relies on the environment variables being set.
    >>> from connectapi import Client
    >>> client = Client()
    Create a client by manually specifying the parameters.
    >>> from connectapi import Client
    >>> client = Client(connect_api_key="XXXX", connect_server="https://colorado.rstudio.com/rsc")
    """    

    @validator("connect_server")
    def validate_connect_server(cls, v):
        return v.rstrip("/")

    @validator("api_endpoint")
    def validate_api_endpoint(cls, v, values):
        if v is None:
            connect_server = values.get("connect_server")
            return f"{connect_server}/__api__/v1"
        else:
            return v

    def create_client(self) -> httpx.Client:
        client = httpx.Client(
            base_url=self.api_endpoint,
            headers={"Authorization": f"Key {self.connect_api_key}"},
        )
        return client


def create_client(
    connect_server: Optional[str] = None,
    connect_api_key: Optional[str] = None,
    api_endpoint: Optional[str] = None
) -> httpx.Client:

    # Validate connect_server.
    if connect_server is None:
        connect_server = os.getenv("CONNECT_SERVER")
    connect_server = connect_server.rstrip("/")

    # Validate connect_api_key
    if connect_api_key is None:
        connect_api_key = os.getenv("CONNECT_API_KEY")

    # Validate api_endpoint
    if api_endpoint is None:
        api_endpoint = f"{connect_server}/__api__/v1"

    return httpx.Client(
        base_url=api_endpoint,
        headers={"Authorization": f"Key {connect_api_key}"},
    )


class Api:
    """Create an interface for calling the Connect API.

    The `Api` class provides the primary interface for calling the Connect API.

    Params
    ------
    connect_server: str | None
        The server endpoint. If `None` connectapi will look for an environment 
        variable `CONNECT_SERVER`. For example 'https://colorado.rstudio.com/rsc'.
        By default, `None`.
    connect_api_key: str | None
        The API key to connect to the Connect server. If `None` connectapi will
        look for an environment variable `CONNECT_API_KEY`. By default, `None`.
    api_endpoint: str | None
        By default connectapi will automatically determine the API endpoint based
        on the `connect_server`. For example if
        `connect_server='https://colorado.rstudio.com/rsc'` is used the
        `api_endpoint` will automatically be set to
        'https://colorado.rstudio.com/rsc/__api__/v1'. However, if you would like
        to override this behaviour your can manually specify the `api_endpoint`.
        For example 'https://colorado.rstudio.com/rsc/api/__api__/v1'. By default,
        `None`.

    Methods
    -------
    content: content.ContentEndpoint
        Exposes the `ContentEndpoint` class for calling content related endpoints.

    Examples
    --------
    Create an API client that relies on the environment variables being set.

    >>> from connectapi import Api
    >>> api = Api

    Create an API client by manually specifying the parameters.

    >>> from connectapi import Api
    >>> client = Api(
    ...    connect_server="https://colorado.rstudio.com/rsc", 
    ...    connect_api_key="XXXX"
    ...)
    
    """    
    content: ContentEndpoint = None

    def __init__(
        self,
        connect_server: Optional[str] = None,
        connect_api_key: Optional[str] = None,
        api_endpoint: Optional[str] = None
    ):
        # Create the httpx.Client
        self.client = create_client(
            connect_server=connect_server,
            connect_api_key=connect_api_key,
            api_endpoint=api_endpoint,
        )

        # Set up all endpoints
        self.content = ContentEndpoint(self.client)


