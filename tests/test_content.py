import pytest
from httpx import HTTPStatusError

from connectapi import Api, Client
from connectapi.content import Content


def test_get_content():
    api = Api()
    r = api.content.list_items(owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
    assert isinstance(r, list)
    assert isinstance(r[0], Content)


def test_get_content_exception():
    client = Client(connect_server="https://google.com")
    api = Api(client)
    with pytest.raises(HTTPStatusError) as error:
        r = api.content.list_items(owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")


def test_get_details():
    api = Api()
    r = api.content.get_details(guid="241fe2cd-6eba-4a79-9aa3-6e6fe28c5714")
    assert isinstance(r, Content)
