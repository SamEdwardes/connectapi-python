from uuid import uuid4

import pytest
from connectapi import Client, Content
from httpx import HTTPStatusError

CONTENT_DATA = {
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

def test_content_create_and_delete():
    client = Client()
    # Create
    content = Content.create(client, **CONTENT_DATA)
    assert isinstance(content, Content)
    assert content.description == 'This report calculates per-team statistics ...'
    assert content.title == 'Quarterly Analysis of Team Velocity'
    # Delete
    content.delete(force=True)
    # Verify that content is gone.
    with pytest.raises(HTTPStatusError) as error:
        Content.get_one(client, content.guid)


def test_content_update():
    client = Client()
    # Create
    content = Content.create(client, **CONTENT_DATA)
    assert isinstance(content, Content)
    assert content.description == 'This report calculates per-team statistics ...'
    assert content.title == 'Quarterly Analysis of Team Velocity'
    # Update
    content.title = "This is a new title"
    content.description = "This is a new description"
    content.update()
    updated_content = Content.get_one(client, content.guid)
    assert updated_content.title == "This is a new title"
    assert updated_content.description == "This is a new description"
    # Delete
    updated_content.delete(force=True)


def test_get_with_owner_guid():
    client = Client()
    contents = Content.get_many(client, owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
    assert len(contents) > 1
    assert isinstance(contents, list)
    assert isinstance(contents[0], Content)


def test_get_no_owner_guid():
    client = Client()
    contents = Content.get_many(client)
    assert len(contents) > 1
    assert isinstance(contents, list)
    assert isinstance(contents[0], Content)


def test_get_with_owner_guid_2_calls():
    client = Client()
    contents_1 = Content.get_many(client, owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
    contents_2 = Content.get_many(client, owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
    assert len(contents_1) == len(contents_2)


def test_get_one():
    client = Client()
    guid = "241fe2cd-6eba-4a79-9aa3-6e6fe28c5714"
    content = Content.get_one(client, content_guid=guid)
    assert isinstance(content, Content)
    assert content.guid == guid


def test_get_content_exception():
    client = Client()
    with pytest.raises(HTTPStatusError) as error:
        r = Content.get_one(client, "XXXXXX")
