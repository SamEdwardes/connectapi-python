import httpx
from pydantic import BaseSettings, validator
from typing import Optional


class Client(BaseSettings):
    connect_api_key: str
    connect_server: str
    api_endpoint: Optional[str]

    @validator("connect_server")
    def validate_connect_server(cls, v):
        return v.rstrip("/")

    @validator("api_endpoint")
    def validate_api_endpoint(cls, v, values):
        if v is None:
            connect_server = values.get('connect_server')
            return f"{connect_server}/__api__/v1"
        else:
            return v

    def create_client(self) -> httpx.Client:
        client = httpx.Client(
            base_url=self.api_endpoint,
            headers={'Authorization': f"Key {self.connect_api_key}"}
        )
        return client
