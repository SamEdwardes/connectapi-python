import os
from textwrap import dedent
from typing import Optional

import httpx


class Client:
    """Create a connection to the Connect server.
    
    Parameters
    ----------
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
        to override this behavior your can manually specify the `api_endpoint`.
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
    
    def __init__(
        self,
        connect_server: Optional[str] = None,
        connect_api_key: Optional[str] = None,
        api_endpoint: Optional[str] = None
    ):
        # Validate connect_server.
        if connect_server is None:
            connect_server = os.getenv("CONNECT_SERVER")
        connect_server = connect_server.rstrip("/")
        self.connect_server = connect_server

        # Validate connect_api_key
        if connect_api_key is None:
            connect_api_key = os.getenv("CONNECT_API_KEY")
        self.connect_api_key = connect_api_key

        # Validate api_endpoint
        if api_endpoint is None:
            api_endpoint = f"{connect_server}/__api__/v1"
        self.api_endpoint = api_endpoint

    def __call__(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.api_endpoint,
            headers={"Authorization": f"Key {self.connect_api_key}"}
        )

    def __str__(self) -> str:
        output = f"""
            Client(
                connect_server='{self.connect_server}',
                connect_api_key='XXXXXXXX',
                api_endpoint='{self.api_endpoint}',
            )
        """
        return dedent(output)

    def __repr__(self) -> str:
        output = self.__str__()
        return (
            output
            .replace(",\n", ", ")
            .replace("\n", "")
            .replace("    ", "")
            .replace(", )", ")")
        )
