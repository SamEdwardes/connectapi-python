import typer
from .client import Client
from .content import Content
from ._console import console
from rich.progress import track
from typing import Optional

app = typer.Typer()
client = Client()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")

@app.command()
def delete(guid: Optional[str] = None):
    """
    Delete content from Connect.
    """
    if guid is None:
        contents = Content.get_my_content(client)
        for content in contents:
            content.delete()
    else:
        content = Content.get_one(client, guid)
        content.delete()
