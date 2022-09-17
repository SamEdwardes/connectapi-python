from connectapi import Client, User

def test_whoami():
    client = Client()
    user = User.whoami(client)
    assert isinstance(user, User)
    assert user.username == "sam.edwardes"