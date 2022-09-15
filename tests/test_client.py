import os

from connectapi import Client


def test_api_trailing_slash():
    os.environ["CONNECT_SERVER"] = "https://colorado.rstudio.com/rsc/"
    client = Client()
    assert str(client().base_url) == "https://colorado.rstudio.com/rsc/__api__/v1/"


def test_api_no_trailing_slash():
    os.environ["CONNECT_SERVER"] = "https://colorado.rstudio.com/rsc"
    client = Client()
    assert str(client().base_url) == "https://colorado.rstudio.com/rsc/__api__/v1/"
