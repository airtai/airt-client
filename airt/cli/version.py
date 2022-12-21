# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/CLI_Version.ipynb.

# %% auto 0
__all__ = ['logger']

# %% ../../notebooks/CLI_Version.ipynb 3
from typing import *

# %% ../../notebooks/CLI_Version.ipynb 4
import typer
import logging
from tabulate import tabulate
import pandas as pd

from airt.client import Client
from airt.logger import get_logger, set_level

# %% ../../notebooks/CLI_Version.ipynb 6
app = typer.Typer()

# %% ../../notebooks/CLI_Version.ipynb 8
logger = get_logger(__name__)

# %% ../../notebooks/CLI_Version.ipynb 11
def version() -> None:
    """Return the server and client versions."""
    try:
        df = pd.Series(Client.version(), name="Version").to_frame()

        typer.echo(tabulate(df, headers="keys", tablefmt="plain"))

    except Exception as e:
        typer.echo(message=f"Error: {e}", err=True)
        raise typer.Exit(code=1)

# %% ../../notebooks/CLI_Version.ipynb 12
app.command()(version)
