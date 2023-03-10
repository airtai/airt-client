# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/CLI_Pred.ipynb.

# %% auto 0
__all__ = ['logger']

# %% ../../notebooks/CLI_Pred.ipynb 3
from typing import *

# %% ../../notebooks/CLI_Pred.ipynb 4
import os

import pandas as pd
import typer
from tabulate import tabulate
from typer import echo

from airt._cli import helper
from airt._constant import CLIENT_DB_PASSWORD, CLIENT_DB_USERNAME
from airt._logger import get_logger, set_level

# %% ../../notebooks/CLI_Pred.ipynb 6
app = typer.Typer(
    help="A set of commands for managing and downloading the predictions."
)

# %% ../../notebooks/CLI_Pred.ipynb 8
logger = get_logger(__name__)

# %% ../../notebooks/CLI_Pred.ipynb 12
@app.command()
@helper.display_formated_table
@helper.requires_auth_token
def ls(
    offset: int = typer.Option(
        0,
        "--offset",
        "-o",
        help="The number of predictions to offset at the beginning. If None, then the default value **0** will be used.",
    ),
    limit: int = typer.Option(
        100,
        "--limit",
        "-l",
        help="The maximum number of predictions to return from the server. If None, "
        "then the default value **100** will be used.",
    ),
    disabled: bool = typer.Option(
        False,
        "--disabled",
        help="If set to **True**, then only the deleted predictions will be returned. Else, the default value "
        "**False** will be used to return only the list of active predictions.",
    ),
    completed: bool = typer.Option(
        False,
        "--completed",
        help="If set to **True**, then only the predictions that are successfully downloaded "
        "to the server will be returned. Else, the default value **False** will be used to "
        "return all the predictions.",
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help="Format output and show only the given column(s) values.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Output only prediction uuids separated by space.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> Dict["str", Union[pd.DataFrame, str]]:
    """Return the list of predictions."""

    from airt.client import Prediction

    predx = Prediction.ls(
        offset=offset, limit=limit, disabled=disabled, completed=completed
    )

    df = Prediction.as_df(predx)

    df["created"] = helper.humanize_date(df["created"])

    return {"df": df, "quite_column_name": "prediction_uuid"}

# %% ../../notebooks/CLI_Pred.ipynb 20
@app.command()
@helper.display_formated_table
@helper.requires_auth_token
def details(
    uuid: str = typer.Argument(
        ...,
        help="Prediction uuid.",
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help="Format output and show only the given column(s) values.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> Dict["str", Union[pd.DataFrame, str]]:
    """Return the details of a prediction."""

    from airt.client import Prediction

    pred = Prediction(uuid=uuid)
    df = pred.details()

    df["created"] = helper.humanize_date(df["created"])

    return {"df": df}

# %% ../../notebooks/CLI_Pred.ipynb 24
@app.command()
@helper.display_formated_table
@helper.requires_auth_token
def rm(
    uuid: str = typer.Argument(
        ...,
        help="Prediction uuid.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Output the deleted Prediction uuid only.",
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help="Format output and show only the given column(s) values.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> Dict["str", Union[pd.DataFrame, str]]:
    """Delete a prediction from the server."""

    from airt.client import Prediction

    pred = Prediction(uuid=uuid)
    df = pred.delete()

    df["created"] = helper.humanize_date(df["created"])

    return {"df": df, "quite_column_name": "prediction_uuid"}

# %% ../../notebooks/CLI_Pred.ipynb 28
@app.command("to-pandas")
@helper.requires_auth_token
def to_pandas(
    uuid: str = typer.Argument(
        ...,
        help="Prediction uuid.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> None:
    """Return the prediction results as a pandas DataFrame."""

    from airt.client import Prediction

    pred = Prediction(uuid=uuid)

    df = pred.to_pandas()

    typer.echo(tabulate(df, headers="keys", tablefmt="plain", showindex=False))  # type: ignore

# %% ../../notebooks/CLI_Pred.ipynb 32
@app.command("to-s3")
@helper.requires_auth_token
def to_s3(
    uuid: str = typer.Argument(
        ...,
        help="Prediction uuid.",
    ),
    uri: str = typer.Option(..., help="The target S3 bucket uri."),
    access_key: Optional[str] = typer.Option(
        None,
        help="Access key for the target S3 bucket. If **None** (default value), then the value from **AWS_ACCESS_KEY_ID** environment variable is used.",
    ),
    secret_key: Optional[str] = typer.Option(
        None,
        help="Secret key for the target S3 bucket. If **None** (default value), then the value from **AWS_SECRET_ACCESS_KEY** environment variable is used.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Output status only.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> None:
    """Push the prediction results to the target AWS S3 bucket."""

    from airt.client import Prediction

    pred = Prediction(uuid=uuid)

    status = pred.to_s3(uri=uri, access_key=access_key, secret_key=secret_key)

    if quiet:
        status.wait()
        typer.echo(f"{pred.uuid}")
    else:
        typer.echo(
            f"Pushing the results for Prediction uuid: {pred.uuid} to the s3 bucket."
        )
        status.progress_bar()

# %% ../../notebooks/CLI_Pred.ipynb 36
@app.command("to-azure-blob-storage")
@helper.requires_auth_token
def to_azure_blob_storage(
    uuid: str = typer.Argument(
        ...,
        help="Prediction uuid.",
    ),
    uri: str = typer.Option(..., help="Target Azure Blob Storage uri."),
    credential: str = typer.Option(
        ...,
        "--credential",
        "-c",
        help="Credential to access the Azure Blob Storage.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Output status only.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> None:
    """Push the prediction results to the target Azure Blob Storage."""

    from airt.client import Prediction

    pred = Prediction(uuid=uuid)
    status = pred.to_azure_blob_storage(uri=uri, credential=credential)

    if quiet:
        status.wait()
        typer.echo(f"{pred.uuid}")
    else:
        typer.echo(
            f"Pushing the results for Prediction uuid: {pred.uuid} to the Azure Blob Storage."
        )
        status.progress_bar()

# %% ../../notebooks/CLI_Pred.ipynb 40
@app.command("to-local")
@helper.requires_auth_token
def to_local(
    uuid: str = typer.Argument(
        ...,
        help="Prediction uuid.",
    ),
    path: str = typer.Option(..., help="Local directory path."),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Output status only.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> None:
    """Download the prediction results to a local directory."""

    from airt.client import Prediction

    pred = Prediction(uuid=uuid)

    if quiet:
        pred.to_local(path=path, show_progress=False)
        typer.echo(f"{pred.uuid}")
    else:
        typer.echo(f"Downloading prediction results for uuid: {pred.uuid}.")
        pred.to_local(path=path)

# %% ../../notebooks/CLI_Pred.ipynb 44
@app.command("to-mysql")
@helper.requires_auth_token
def to_mysql(
    uuid: str = typer.Argument(
        ...,
        help="Prediction uuid.",
    ),
    host: str = typer.Option(..., help="Database host name."),
    database: str = typer.Option(..., help="Database name."),
    table: str = typer.Option(..., help="Table name."),
    port: int = typer.Option(
        3306,
        help="Host port number. If not passed, then the default value **3306** will be used.",
    ),
    username: Optional[str] = typer.Option(
        None,
        "--username",
        "-u",
        help="Database username. If not passed, then the value set in the environment variable"
        f" **{CLIENT_DB_USERNAME}** will be used else the default value **root** will be used.",
    ),
    password: Optional[str] = typer.Option(
        None,
        "--password",
        "-p",
        help="Database password. If not passed, then the value set in the environment variable"
        f' **{CLIENT_DB_PASSWORD}** will be used else the default value "" will be used.',
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Output status only.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> None:
    """Push the prediction results to a mysql database.

    If the database requires authentication, pass the username/password as commandline arguments or store it in
    the **AIRT_CLIENT_DB_USERNAME** and **AIRT_CLIENT_DB_PASSWORD** environment variables.
    """

    from airt.client import Prediction

    pred = Prediction(uuid=uuid)

    status = pred.to_mysql(
        host=host,
        database=database,
        table=table,
        port=port,
        username=username,
        password=password,
    )

    if quiet:
        status.wait()
        typer.echo(f"{pred.uuid}")
    else:
        typer.echo(
            f"Pushing the results for Prediction uuid: {pred.uuid} to the mysql database."
        )
        status.progress_bar()

# %% ../../notebooks/CLI_Pred.ipynb 47
@app.command("to-clickhouse")
@helper.requires_auth_token
def to_clickhouse(
    uuid: str = typer.Argument(
        ...,
        help="Prediction uuid.",
    ),
    host: str = typer.Option(..., help="Remote database host name."),
    database: str = typer.Option(..., help="Database name."),
    table: str = typer.Option(..., help="Table name."),
    protocol: str = typer.Option(..., help="Protocol to use (native/http)."),
    port: int = typer.Option(
        0,
        help="Host port number. If not passed, then the default value **0** will be used.",
    ),
    username: Optional[str] = typer.Option(
        None,
        "--username",
        "-u",
        help="Database username. If not passed, then the value set in the environment variable"
        " **CLICKHOUSE_USERNAME** will be used else the default value **root** will be used.",
    ),
    password: Optional[str] = typer.Option(
        None,
        "--password",
        "-p",
        help="Database password. If not passed, then the value set in the environment variable"
        ' **CLICKHOUSE_PASSWORD** will be used else the default value "" will be used.',
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Output status only.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> None:
    """Push the prediction results to a clickhouse database.

    If the database requires authentication, pass the username/password as commandline arguments or store it in
    the **CLICKHOUSE_USERNAME** and **CLICKHOUSE_PASSWORD** environment variables.
    """

    from airt.client import Prediction

    pred = Prediction(uuid=uuid)

    status = pred.to_clickhouse(
        host=host,
        database=database,
        table=table,
        port=port,
        protocol=protocol,
        username=username,
        password=password,
    )

    if quiet:
        status.wait()
        typer.echo(f"{pred.uuid}")
    else:
        typer.echo(
            f"Pushing the results for Prediction uuid: {pred.uuid} to the clickhouse database."
        )
        status.progress_bar()
