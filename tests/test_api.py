import os

from connectapi import Api


def test_api_trailing_slash():
    os.environ["CONNECT_SERVER"] = "https://colorado.rstudio.com/rsc/"
    api = Api()
    assert str(api.client.base_url) == "https://colorado.rstudio.com/rsc/__api__/v1/"


def test_api_no_trailing_slash():
    os.environ["CONNECT_SERVER"] = "https://colorado.rstudio.com/rsc"
    api = Api()
    assert str(api.client.base_url) == "https://colorado.rstudio.com/rsc/__api__/v1/"
