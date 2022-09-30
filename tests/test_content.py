from uuid import uuid4

import pytest
from connectapi import Client, Content
from httpx import HTTPStatusError


def test_content_create_and_delete():
    client = Client()

    # Create
    data = {
        'access_type': 'acl',
        'connection_timeout': 3600,
        'description': 'This report calculates per-team statistics ...',
        'idle_timeout': 5,
        'init_timeout': 60,
        'load_factor': 0.5,
        'max_conns_per_process': 20,
        'max_processes': 3,
        'min_processes': 0,
        'name': str(uuid4()),
        'read_timeout': 3600,
        'run_as': 'rstudio-connect',
        'run_as_current_user': False,
        'title': 'Quarterly Analysis of Team Velocity'
    }
    content = Content.create(client, **data)
    assert isinstance(content, Content)
    assert content.description == 'This report calculates per-team statistics ...'
    assert content.title == 'Quarterly Analysis of Team Velocity'

    # Delete
    content.delete(force=True)

    # Verify that content is gone.
    with pytest.raises(HTTPStatusError) as error:
        Content.get_one(client, content.guid)




def test_get_with_owner_guid():
    client = Client()
    contents = Content.get(client, owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
    assert len(contents) > 1
    assert isinstance(contents, list)
    assert isinstance(contents[0], Content)


def test_get_no_owner_guid():
    client = Client()
    contents = Content.get(client)
    assert len(contents) > 1
    assert isinstance(contents, list)
    assert isinstance(contents[0], Content)


# def test_get_with_owner_guid_2_calls():
#     client = Client()
#     contents_1 = Content.get(client, owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
#     contents_2 = Content.get(client, owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
#     assert len(contents_1) == len(contents_2)


def test_get_one():
    client = Client()
    guid = "241fe2cd-6eba-4a79-9aa3-6e6fe28c5714"
    content = Content.get_one(client, content_guid=guid)
    assert isinstance(content, Content)
    assert content.guid == guid





# def test_list_items():
#     api = Api()
#     r = api.content.list_items(owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
#     assert isinstance(r, list)
#     assert isinstance(r[0], Content)


# def test_get_content_exception():
#     api = Api(connect_server="https://google.com")
#     with pytest.raises(HTTPStatusError) as error:
#         r = api.content.list_items(owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")


# def test_get_details():
#     api = Api()
#     r = api.content.get_details(guid="241fe2cd-6eba-4a79-9aa3-6e6fe28c5714")
#     assert isinstance(r, Content)


# def test_create_item():
#     data = {
#         'access_type': 'acl',
#         'connection_timeout': 3600,
#         'description': 'This report calculates per-team statistics ...',
#         'idle_timeout': 5,
#         'init_timeout': 60,
#         'load_factor': 0.5,
#         'max_conns_per_process': 20,
#         'max_processes': 3,
#         'min_processes': 0,
#         'name': 'quarterly-analysis',
#         'read_timeout': 3600,
#         'run_as': 'rstudio-connect',
#         'run_as_current_user': False,
#         'title': 'Quarterly Analysis of Team Velocity'
#     }
#     api = Api()
#     r = api.content.get_details(guid="241fe2cd-6eba-4a79-9aa3-6e6fe28c5714")
