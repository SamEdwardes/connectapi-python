from connectapi import Client, User, Content

def test_whoami():
    client = Client()
    user = User.whoami(client)
    assert isinstance(user, User)
    assert user.username == "sam.edwardes"

def test_my_content():
    client = Client()
    user = User.whoami(client)
    assert user.username == "sam.edwardes"
    my_content = user.get_my_content()
    assert isinstance(my_content, list)
    assert isinstance(my_content[0], Content)