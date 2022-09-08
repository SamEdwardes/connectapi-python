import os

from connectapi import Client


def test_settings_trailing_slash():
    os.environ["CONNECT_SERVER"] = "https://colorado.rstudio.com/rsc/"
    client = Client()
    assert client.connect_server == "https://colorado.rstudio.com/rsc"
    assert client.api_endpoint == "https://colorado.rstudio.com/rsc/__api__/v1"


def test_settings_no_trailing_slash():
    os.environ["CONNECT_SERVER"] = "https://colorado.rstudio.com/rsc/"
    client = Client()
    assert client.connect_server == "https://colorado.rstudio.com/rsc"
    assert client.api_endpoint == "https://colorado.rstudio.com/rsc/__api__/v1"
