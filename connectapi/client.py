from typing import Optional

import httpx
from pydantic import BaseSettings, validator


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
