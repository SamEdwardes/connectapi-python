# import pytest
# from httpx import HTTPStatusError

# from connectapi import Client, Content


# def test_get_content_exception():
#     client = Client(connect_server="https://google.com")
#     with pytest.raises(HTTPStatusError) as error:
#         r = client.content.list_items(owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
