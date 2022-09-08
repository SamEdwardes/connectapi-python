from connectapi.api import Api
from connectapi import models


def test_get_content():
    api = Api()
    r = api.content.get_content(owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
    assert isinstance(r, list)
    assert isinstance(r[0], models.content.Content)


def test_get_details():
    api = Api()
    r = api.content.get_details(guid="241fe2cd-6eba-4a79-9aa3-6e6fe28c5714")
    assert isinstance(r, models.content.Content)
