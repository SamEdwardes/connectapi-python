from pydantic import BaseModel, BaseSettings, validator
from rich import print, inspect


class Settings(BaseSettings):
    connect_api_key: str
    connect_server: str
    api_endpoint: str = None

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