import pytest
from httpx import HTTPStatusError

from connectapi import Api, Client, models


def test_get_content_exception():
    client = Client(connect_server="https://google.com")
    api = Api(client)
    with pytest.raises(HTTPStatusError) as error:
        r = api.content.get_content(owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
