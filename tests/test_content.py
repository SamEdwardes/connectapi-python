from connectapi.content import get_details, get_content


def test_get_content():
    r = get_content(owner_guid="d03a6b7a-c818-4e40-8ef9-84ca567f9671")
    assert r.response.status_code == 200


def test_get_details():
    r = get_details(guid="241fe2cd-6eba-4a79-9aa3-6e6fe28c5714")
    assert r.response.status_code == 200
