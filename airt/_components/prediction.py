# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/API_Prediction.ipynb.

# %% auto 0
__all__ = ['Prediction']

# %% ../../notebooks/API_Prediction.ipynb 4
from typing import *

# %% ../../notebooks/API_Prediction.ipynb 5
import os
import textwrap
from pathlib import Path

import pandas as pd
import requests
from fastcore.foundation import patch
from tqdm import tqdm

from airt._components.client import Client
from airt._components.progress_status import ProgressStatus
from airt._constant import CLIENT_DB_PASSWORD, CLIENT_DB_USERNAME
from airt._helper import (
    add_example_to_docs,
    add_ready_column,
    delete_data,
    generate_df,
    get_attributes_from_instances,
    get_data,
    post_data,
    export,
)
from airt._logger import get_logger, set_level

# %% ../../notebooks/API_Prediction.ipynb 7
logger = get_logger(__name__)

# %% ../../notebooks/API_Prediction.ipynb 10
@export("airt.client")
class Prediction(ProgressStatus):
    """A class to manage and download the predictions.

    The **Prediction** class is automatically instantiated by calling the `Model.predict` method of a `Model` instance.
    Currently, it is the only way to instantiate this class.

    At the moment, the prediction results can only be

    - downloaded to a local folder in parquet file format

    - pushed to Azure Blob Storage or an AWS S3 bucket

    - pushed to MySql or ClickHouse database

    We intend to support additional databases and storage mediums in future releases.
    """

    BASIC_PRED_COLS = ["uuid", "created", "total_steps", "completed_steps"]
    ALL_PRED_COLS = BASIC_PRED_COLS + [
        "model",
        "datasource",
        "region",
        "cloud_provider",
        "error",
    ]

    COLS_TO_RENAME = {
        "uuid": "prediction_uuid",
        "datasource": "datasource_uuid",
        "model": "model_uuid",
    }

    def __init__(
        self,
        uuid: str,
        datasource: Optional[str] = None,
        model: Optional[str] = None,
        created: Optional[str] = None,
        total_steps: Optional[int] = None,
        completed_steps: Optional[int] = None,
        region: Optional[str] = None,
        cloud_provider: Optional[str] = None,
        error: Optional[str] = None,
        disabled: Optional[bool] = None,
    ):
        """Constructs a new **Prediction** instance

        Warning:
            Do not construct this object directly by calling the constructor, instead please use
            `Model.predict` method of the Model instance.

        Args:
            uuid: Prediction uuid.
            datasource: DataSource uuid.
            model: Model uuid.
            created: Prediction creation date.
            total_steps: No of steps needed to complete the model prediction.
            completed_steps: No of steps completed so far in the model prediction.
            region: The region name of the cloud provider where the prediction is stored.
            cloud_provider: The name of the cloud storage provider where the prediction is stored.
            error: Contains the error message if running the predictions fails.
            disabled: A flag that indicates the prediction's status. If the prediction is deleted, then **False** will be set.
        """
        self.uuid = uuid
        self.datasource = datasource
        self.model = model
        self.created = created
        self.total_steps = total_steps
        self.completed_steps = completed_steps
        self.region = region
        self.cloud_provider = cloud_provider
        self.error = error
        self.disabled = disabled
        ProgressStatus.__init__(self, relative_url=f"/prediction/{self.uuid}")

    @staticmethod
    def _download_prediction_file_to_local(
        file_name: str, url: str, path: Union[str, Path]
    ) -> None:
        """Download the file to local directory.

        Args:
            file_name: Name of the file
            url: Url of the file
            path: Local directory path

        Raises:
            HTTPError: If the **url** is invalid or not reachable.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(e)

        else:
            with open(Path(path) / file_name, "wb") as f:
                f.write(response.content)

    @staticmethod
    def ls(
        offset: int = 0,
        limit: int = 100,
        disabled: bool = False,
        completed: bool = False,
    ) -> List["Prediction"]:
        """Return the list of Prediction instances available in the server.

        Args:
            offset: The number of predictions to offset at the beginning. If None, then the default value **0** will be used.
            limit: The maximum number of predictions to return from the server. If None,
                then the default value **100** will be used.
            disabled: If set to **True**, then only the deleted predictions will be returned. Else, the default value
                **False** will be used to return only the list of active predictions.
            completed: If set to **True**, then only the predictions that are successfully processed in server will be returned.
                Else, the default value **False** will be used to return all the predictions.

        Returns:
            A list of Prediction instances available in the server.

        Raises:
            ConnectionError: If the server address is invalid or not reachable.
        """
        lists = Client._get_data(
            relative_url=f"/prediction/?disabled={disabled}&completed={completed}&offset={offset}&limit={limit}"
        )

        predx = [
            Prediction(
                uuid=pred["uuid"],
                model=pred["model"],
                datasource=pred["datasource"],
                created=pred["created"],
                total_steps=pred["total_steps"],
                completed_steps=pred["completed_steps"],
                region=pred["region"],
                cloud_provider=pred["cloud_provider"],
                error=pred["error"],
                disabled=pred["disabled"],
            )
            for pred in lists
        ]

        return predx

    @staticmethod
    def as_df(predx: List["Prediction"]) -> pd.DataFrame:
        """Return the details of prediction instances as a pandas dataframe.

        Args:
            predx: List of prediction instances.

        Returns:
            Details of all the prediction in a dataframe.

        Raises:
            ConnectionError: If the server address is invalid or not reachable.
        """
        response = get_attributes_from_instances(predx, Prediction.BASIC_PRED_COLS)  # type: ignore

        df = generate_df(response, Prediction.BASIC_PRED_COLS)

        df = df.rename(columns=Prediction.COLS_TO_RENAME)

        return add_ready_column(df)

    def details(self) -> pd.DataFrame:
        raise NotImplementedError()

    def to_pandas(self) -> pd.DataFrame:
        raise NotImplementedError()

    def delete(self) -> pd.DataFrame:
        raise NotImplementedError()

    def to_s3(
        self,
        uri: str,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> ProgressStatus:
        raise NotImplementedError()

    def to_azure_blob_storage(
        self,
        uri: str,
        credential: Optional[str] = None,
    ) -> ProgressStatus:
        raise NotImplementedError()

    def to_local(
        self,
        path: Union[str, Path],
        show_progress: Optional[bool] = True,
    ) -> None:
        raise NotImplementedError()

    def to_mysql(
        self,
        *,
        host: str,
        database: str,
        table: str,
        port: int = 3306,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> ProgressStatus:
        raise NotImplementedError()

    def to_clickhouse(
        self,
        *,
        host: str,
        database: str,
        table: str,
        port: int = 0,
        protocol: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> ProgressStatus:
        raise NotImplementedError()

# %% ../../notebooks/API_Prediction.ipynb 11
def _docstring_example():
    """
    Example:
        ```python
        # Importing necessary libraries
        import os
        import tempfile
        from datetime import timedelta

        from azure.identity import DefaultAzureCredential
        from azure.mgmt.storage import StorageManagementClient

        from  airt.client import Client, DataBlob, DataSource, Model, Prediction

        # Authenticate
        Client.get_token(username="{fill in username}", password="{fill in password}")

        # Create a datablob
        # In this example, the datablob will be stored in an AWS S3 bucket. The
        # access_key and the secret_key are set in the AWS_ACCESS_KEY_ID and
        # AWS_SECRET_ACCESS_KEY environment variables, and the region is set to
        # eu-west-3; feel free to change the cloud provider and the region to
        # suit your needs.
        db = DataBlob.from_s3(
            uri="{fill in uri}",
            cloud_provider="aws",
            region="eu-west-3"
        )

        # Display the status in a progress bar
        db.progress_bar()

        # Create a datasource
        ds = db.to_datasource(
            file_type="{fill in file_type}",
            index_column="{fill in index_column}",
            sort_by="{fill in sort_by}",
        )

        # Display the status in a progress bar
        ds.progress_bar()

        # Train a model to predicts which users will perform a purchase
        # event ("*purchase") three hours before they actually do it.
        model = ds.train(
            client_column="{fill in client_column}",
            target_column="{fill in target_column}",
            target="*purchase",
            predict_after=timedelta(hours=3)
        )

        # Display the status in a progress bar
        model.progress_bar()

        # Run predictions
        prediction = model.predict()
        prediction.progress_bar()

        # Print the details of the newly created prediction
        print(prediction.details())

        # Get the list of all prediction instances created by the currently logged-in user
        predx = Prediction.ls()
        print(predx)

        # Display the details of the prediction instances in a pandas dataframe
        df = Prediction.as_df(predx)
        print(df)

        # Display the prediction results in a pandas DataFrame
        print(prediction.to_pandas())

        # Push the prediction results to an AWS S3 bucket
        s3_status = prediction.to_s3(uri="{fill in s3_target_uri}")

        # Push the prediction results to an Azure Blob Storage
        os.environ["AZURE_SUBSCRIPTION_ID"] = "{fill in azure_subscription_id}"
        os.environ["AZURE_CLIENT_ID"] = "{fill in azure_client_id}"
        os.environ["AZURE_CLIENT_SECRET"] = "{fill in azure_client_secret}"
        os.environ["AZURE_TENANT_ID"]= "{fill in azure_tenant_id}"
        azure_group_name = "{fill in azure_group_name}"
        azure_storage_account_name = "{fill in azure_storage_account_name}"
        azure_storage_client = StorageManagementClient(
            DefaultAzureCredential(), os.environ["AZURE_SUBSCRIPTION_ID"]
        )
        azure_storage_keys = azure_storage_client.storage_accounts.list_keys(
            azure_group_name, azure_storage_account_name
        )
        azure_storage_keys = {v.key_name: v.value for v in azure_storage_keys.keys}
        azure_credential = azure_storage_keys['key1']

        azure_status = prediction.to_azure_blob_storage(
            uri="{fill in azure_target_uri}",
            credential=azure_credential
        )

        # Push the prediction results to a MySQL database
        mysql_status = prediction.to_mysql(
            username="{fill in mysql_db_username}",
            password="{fill in mysql_db_password}",
            host="{fill in mysql_host}",
            database="{fill in mysql_database}",
            table="{fill in mysql_table}",
        )

        # Push the prediction results to a ClickHouse database
        clickhouse_status = prediction.to_clickhouse(
            username="{fill in clickhouse_db_username}",
            password="{fill in clickhouse_db_password}",
            host="{fill in clickhouse_host}",
            database="{fill in clickhouse_database}",
            table="{fill in clickhouse_table}",
            protocol="native",
        )

        # Download the predictions to a local directory
        # In this example, the prediction results are downloaded
        # to a temporary directory
        with tempfile.TemporaryDirectory(prefix="predictions_results_") as d:
            prediction.to_local(path=d)
            # Check the downloaded prediction files
            downloaded_files = sorted(list(os.listdir(d)))
            print(downloaded_files)


        # Check the status
        s3_status.wait()
        azure_status.progress_bar()
        mysql_status.progress_bar()
        clickhouse_status.progress_bar()

        # Delete the prediction
        prediction.delete()
        ```
    """
    pass

# %% ../../notebooks/API_Prediction.ipynb 13
add_example_to_docs(Prediction, _docstring_example.__doc__)  # type: ignore
add_example_to_docs(Prediction.ls, _docstring_example.__doc__)  # type: ignore
add_example_to_docs(Prediction.as_df, _docstring_example.__doc__)  # type: ignore

# %% ../../notebooks/API_Prediction.ipynb 17
@patch
def details(self: Prediction) -> pd.DataFrame:
    """Return the details of a prediction.

    Returns:
        A pandas DataFrame encapsulating the details of the prediction.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.
    """
    response = Client._get_data(relative_url=f"/prediction/{self.uuid}")

    df = pd.DataFrame(response, index=[0])[Prediction.ALL_PRED_COLS]

    df = df.rename(columns=Prediction.COLS_TO_RENAME)

    return add_ready_column(df)

# %% ../../notebooks/API_Prediction.ipynb 18
add_example_to_docs(Prediction.details, _docstring_example.__doc__)  # type: ignore

# %% ../../notebooks/API_Prediction.ipynb 21
@patch
def delete(self: Prediction) -> pd.DataFrame:
    """Delete a prediction from the server.

    Returns:
        A pandas DataFrame encapsulating the details of the deleted prediction.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.
    """
    response = Client._delete_data(relative_url=f"/prediction/{self.uuid}")

    df = pd.DataFrame(response, index=[0])[Prediction.BASIC_PRED_COLS]

    df = df.rename(columns=Prediction.COLS_TO_RENAME)

    return add_ready_column(df)

# %% ../../notebooks/API_Prediction.ipynb 22
add_example_to_docs(Prediction.delete, _docstring_example.__doc__)  # type: ignore

# %% ../../notebooks/API_Prediction.ipynb 28
@patch
def to_pandas(self: Prediction) -> pd.DataFrame:
    """Return the prediction results as a pandas DataFrame

    Returns:
        A pandas DataFrame encapsulating the results of the prediction.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.
    """
    response = Client._get_data(relative_url=f"/prediction/{self.uuid}/pandas")
    keys = list(response.keys())
    keys.remove("Score")
    index_name = keys[0]
    return (
        pd.DataFrame(response)
        .set_index(index_name)
        .sort_values("Score", ascending=False)
    )

# %% ../../notebooks/API_Prediction.ipynb 29
add_example_to_docs(Prediction.to_pandas, _docstring_example.__doc__)  # type: ignore

# %% ../../notebooks/API_Prediction.ipynb 31
@patch
def to_s3(
    self: Prediction,
    uri: str,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
) -> ProgressStatus:
    """Push the prediction results to the target AWS S3 bucket.

    Args:
        uri: Target S3 bucket uri.
        access_key: Access key for the target S3 bucket. If **None** (default value), then the value
            from **AWS_ACCESS_KEY_ID** environment variable is used.
        secret_key: Secret key for the target S3 bucket. If **None** (default value), then the value
            from **AWS_SECRET_ACCESS_KEY** environment variable is used.

    Returns:
        An instance of `ProgressStatus` class.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.
    """
    access_key = (
        access_key if access_key is not None else os.environ["AWS_ACCESS_KEY_ID"]
    )
    secret_key = (
        secret_key if secret_key is not None else os.environ["AWS_SECRET_ACCESS_KEY"]
    )

    response = Client._post_data(
        relative_url=f"/prediction/{self.uuid}/to_s3",
        json=dict(uri=uri, access_key=access_key, secret_key=secret_key),
    )

    return ProgressStatus(relative_url=f"/prediction/push/{response['uuid']}")

# %% ../../notebooks/API_Prediction.ipynb 32
add_example_to_docs(Prediction.to_s3, _docstring_example.__doc__)  # type: ignore

# %% ../../notebooks/API_Prediction.ipynb 35
@patch
def to_azure_blob_storage(
    self: Prediction,
    uri: str,
    credential: str,
) -> ProgressStatus:
    """Push the prediction results to the target Azure Blob Storage.

    Args:
        uri: Target Azure Blob Storage uri.
        credential: Credential to access the Azure Blob Storage.

    Returns:
        An instance of `ProgressStatus` class.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.
    """
    response = Client._post_data(
        relative_url=f"/prediction/{self.uuid}/to_azure_blob_storage",
        json=dict(uri=uri, credential=credential),
    )

    return ProgressStatus(relative_url=f"/prediction/push/{response['uuid']}")

# %% ../../notebooks/API_Prediction.ipynb 36
add_example_to_docs(Prediction.to_azure_blob_storage, _docstring_example.__doc__)  # type: ignore

# %% ../../notebooks/API_Prediction.ipynb 39
@patch
def to_local(
    self: Prediction,
    path: Union[str, Path],
    show_progress: Optional[bool] = True,
) -> None:
    """Download the prediction results to a local directory.

    Args:
        path: Local directory path.
        show_progress: Flag to set the progressbar visibility. If not passed, then the default value **True** will be used.

    Raises:
        FileNotFoundError: If the **path** is invalid.
        HTTPError: If the presigned AWS s3 uri to download the prediction results are invalid or not reachable.
    """
    response = Client._get_data(relative_url=f"/prediction/{self.uuid}/to_local")

    # Initiate progress bar
    t = tqdm(total=len(response), disable=not show_progress)

    for file_name, url in response.items():
        Prediction._download_prediction_file_to_local(file_name, url, Path(path))
        t.update()

    t.close()

# %% ../../notebooks/API_Prediction.ipynb 40
add_example_to_docs(Prediction.to_local, _docstring_example.__doc__)  # type: ignore

# %% ../../notebooks/API_Prediction.ipynb 43
@patch
def to_mysql(
    self: Prediction,
    *,
    host: str,
    database: str,
    table: str,
    port: int = 3306,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> ProgressStatus:
    """Push the prediction results to a mysql database.

    If the database requires authentication, pass the username/password as parameters or store it in
    the **AIRT_CLIENT_DB_USERNAME** and **AIRT_CLIENT_DB_PASSWORD** environment variables.

    Args:
        host: Database host name.
        database: Database name.
        table: Table name.
        port: Host port number. If not passed, then the default value **3306** will be used.
        username: Database username. If not passed, then the value set in the environment variable
            **AIRT_CLIENT_DB_USERNAME** will be used else the default value "root" will be used.
        password: Database password. If not passed, then the value set in the environment variable
            **AIRT_CLIENT_DB_PASSWORD** will be used else the default value "" will be used.

    Returns:
        An instance of `ProgressStatus` class.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.
    """
    username = (
        username if username is not None else os.environ.get(CLIENT_DB_USERNAME, "root")
    )

    password = (
        password if password is not None else os.environ.get(CLIENT_DB_PASSWORD, "")
    )

    req_json = dict(
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
        table=table,
    )

    response = Client._post_data(
        relative_url=f"/prediction/{self.uuid}/to_mysql", json=req_json
    )

    return ProgressStatus(relative_url=f"/prediction/push/{response['uuid']}")

# %% ../../notebooks/API_Prediction.ipynb 44
add_example_to_docs(Prediction.to_mysql, _docstring_example.__doc__)  # type: ignore

# %% ../../notebooks/API_Prediction.ipynb 47
@patch
def to_clickhouse(
    self: Prediction,
    *,
    host: str,
    database: str,
    table: str,
    protocol: str,
    port: int = 0,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> ProgressStatus:
    """Push the prediction results to a clickhouse database.

    If the database requires authentication, pass the username/password as parameters or store it in
    the **CLICKHOUSE_USERNAME** and **CLICKHOUSE_PASSWORD** environment variables.

    Args:
        host: Remote database host name.
        database: Database name.
        table: Table name.
        protocol: Protocol to use (native/http).
        port: Host port number. If not passed, then the default value **0** will be used.
        username: Database username. If not passed, then the value set in the environment variable
            **CLICKHOUSE_USERNAME** will be used else the default value "root" will be used.
        password: Database password. If not passed, then the value set in the environment variable
            **CLICKHOUSE_PASSWORD** will be used else the default value "" will be used.

    Returns:
        An instance of `ProgressStatus` class.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.
    """
    username = (
        username
        if username is not None
        else os.environ.get("CLICKHOUSE_USERNAME", "root")
    )

    password = (
        password if password is not None else os.environ.get("CLICKHOUSE_PASSWORD", "")
    )

    req_json = dict(
        host=host,
        database=database,
        table=table,
        protocol=protocol,
        port=port,
        username=username,
        password=password,
    )

    response = Client._post_data(
        relative_url=f"/prediction/{self.uuid}/to_clickhouse", json=req_json
    )

    return ProgressStatus(relative_url=f"/prediction/push/{response['uuid']}")

# %% ../../notebooks/API_Prediction.ipynb 48
add_example_to_docs(Prediction.to_clickhouse, _docstring_example.__doc__)  # type: ignore
