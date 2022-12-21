# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/API_Helper.ipynb.

# %% auto 0
__all__ = ['ensure_is_instance', 'get_base_url', 'post_data', 'get_data', 'delete_data', 'add_ready_column', 'generate_df',
           'get_values_from_item', 'get_attributes_from_instances', 'dict_to_df', 'standardize_phone_number']

# %% ../notebooks/API_Helper.ipynb 2
from typing import *

# %% ../notebooks/API_Helper.ipynb 3
import os
import requests
from types import MethodType
import textwrap

import pandas as pd

from airt.constant import SERVER_URL, PROD_URL

# %% ../notebooks/API_Helper.ipynb 5
def ensure_is_instance(o: Any, cls: Type):
    """A function to check if the object argument is an instance of the class argument.

    Args:
        o: A python object for which the instance needs to be checked.
        cls: The expected instance of the object argument.

    Raises:
        A TypeError if the object is not an instance of the class type.
    """
    if not isinstance(o, cls):
        raise TypeError(
            f"The parameter must be a {cls} type, but got `{type(o).__name__}`"
        )

# %% ../notebooks/API_Helper.ipynb 7
def _get_json(response: requests.Response) -> Any:
    """A function to validate the status of the response object.

    Args:
        response: The response object that encapsulates the server's response.

    Returns:
        A dictionary of the response body.

    Raises:
        ValueError: If the response code is not in range of 200 - 399.
    """
    if response:
        return response.json()
    else:
        raise ValueError(response.json()["detail"])

# %% ../notebooks/API_Helper.ipynb 11
def get_base_url(server: Optional[str]) -> str:
    """Return the base URL for the airt server.

    If the server value is `None`, retrive the value from the environment variable `AIRT_SERVER_URL`.
    If the variable is not set as well, then the default public server will be used.
    """

    return server if server is not None else os.environ.get(SERVER_URL, PROD_URL)

# %% ../notebooks/API_Helper.ipynb 15
def post_data(
    url: str,
    token: Optional[str],
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """A function to send a POST request.

    Args:
        url: The URL of the server to which the request needs to be sent.
        data: A Dictionary object to send in the body of the POST request. The data sent in this param will automatically be form-encoded by the request library.
        json: A Dictionary object to send in the body of the POST request. The data sent in this param will automatically be JSON-encoded by the request library.
        token: The unique auth token for the client, obtained via calling the `Client.get_token()` method.
            Set it to `None` in `Client.get_token()` to obtain the token.

    Returns:
        A dictionary that encapsulates the response body.

    Raises:
        ConnectionError: If the server is not reachable.
        ValueError: If the response code is not in range of 200 - 399.
    """
    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url, json=json, data=data, headers=headers)
    else:
        response = requests.post(url, data=data, json=json)
    return _get_json(response)

# %% ../notebooks/API_Helper.ipynb 18
def get_data(url: str, token: Optional[str]) -> Any:
    """Send a GET request.

    Args:
        url: The URL of the server to which the request needs to be sent.
        token: The unique auth token for the client, obtained via calling the `Client.get_token()` method.

    Returns:
        A dictionary that encapsulates the response body.

    Raises:
        ConnectionError: If the server is not reachable.
        ValueError: If the response code is not in range of 200 - 399.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return _get_json(response)

# %% ../notebooks/API_Helper.ipynb 20
def delete_data(url: str, token: Optional[str]) -> Dict[str, Any]:
    """Send a DELETE request.

    Args:
        url: The URL of the server to which the request needs to be sent.
        token: The unique auth token for the client, obtained via calling the `Client.get_token()` method.

    Returns:
        A dictionary that encapsulates the response body.

    Raises:
        ConnectionError: If the server is not reachable.
        ValueError: If the response code is not in range of 200 - 399.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    return _get_json(response)

# %% ../notebooks/API_Helper.ipynb 23
def add_ready_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add ready column to the DataFrame

    Args:
        df: A pandas DataFrame with completed_steps and total_steps columns

    Returns:
        A pandas DataFrame with ready column
    """

    df["ready"] = df["completed_steps"] == df["total_steps"]
    return df.drop(columns=["completed_steps", "total_steps"])

# %% ../notebooks/API_Helper.ipynb 25
def generate_df(
    items: Union[Dict[str, Any], List[Dict[str, Any]]], columns: list
) -> pd.DataFrame:
    """Generate a DataFrame based on the items length

    Args:
        items: A list encapsulating the response from an API endpoint that needs to be converted into a DataFrame.
        columns: A list of columns names to be included in the DataFrame.

    Returns:
        A DataFrame with a shape of (items, columns), if the length of the items is > 0, otherwise an empty DataFrame with only columns names.
    """

    if len(items) > 0:
        df = pd.DataFrame(items)[columns]
    else:
        df = pd.DataFrame({c: [] for c in columns})

    return df

# %% ../notebooks/API_Helper.ipynb 27
def get_values_from_item(items: list, value: Optional[str] = None) -> str:
    """Get **values** from items seperated by comma.

    Args:
        items: The item list from the response.
        value: The value to extract from each items.

    Returns:
        The **values** as string seperated by comma. If the tags list is empty, <none> will be returned.
    """

    if len(items) == 0:
        return "<none>"

    if value is None:
        return ", ".join(items)

    return ", ".join([str(i[value]) for i in items])

# %% ../notebooks/API_Helper.ipynb 31
def get_attributes_from_instances(
    ox: List[object], attributes: List[str]
) -> List[Dict[str, Any]]:
    """Extract the **attributes** from the instances.

    Args:
        ox: List of instances.
        attributes: Attributes to extract from the instances as a list

    Returns:
        A list encapsulating the attribute name and value pairs of each instance.
    """

    lists = [{i: getattr(o, i) for i in attributes} for o in ox]
    return lists

# %% ../notebooks/API_Helper.ipynb 33
def dict_to_df(d: Dict[str, Any]) -> pd.DataFrame:
    """Convert the dict into a pandas dataframe

    Args:
        d: Dict containing the data and dtypes

    Returns:
        The pandas dataframe constructed from the dict
    """
    data = d["data"]
    dtypes = d["dtypes"]

    df = pd.DataFrame(
        data=data["data"], index=data["index"], columns=data["columns"]
    ).rename_axis(data["index_names"])

    for k, v in dtypes.items():
        df[k] = df[k].astype(v)

    return df

# %% ../notebooks/API_Helper.ipynb 35
def check_and_append_otp_query_param(relative_url: str, otp: Union[str, None]) -> str:
    """Append the otp query parameter to the relative url if its not None

    Args:
        relative_url: The relative url for the route
        otp: user otp

    Returns:
        The updated relative_url if otp is not None, else returns the original relative_url
    """
    if otp is not None:
        relative_url = (
            (relative_url + f"&otp={otp}")
            if len(relative_url.split("?")) > 1
            else (relative_url + f"?otp={otp}")
        )
    return relative_url

# %% ../notebooks/API_Helper.ipynb 39
def standardize_phone_number(phone_number: str) -> str:
    """Standardize the user's phone number

    This function takes the user's phone number in different formats and converts it into a
    standardized format. For example, the user can enter the phone number as **440123456789, +440123456789,
    00440123456789, +44 0123456789, and (+44) 012 345 6789** to register a UK-based phone number and this function takes the user input and
    converts it into 440123456789 standardized format.

    Args:
        phone_number: The phone number to convert into a standardized format.

    Returns:
        The phone number in a standardized format.
    """
    phone_number = "".join(filter(str.isdigit, phone_number))
    if phone_number.startswith("00"):
        phone_number = phone_number[2:]
    return phone_number

# %% ../notebooks/API_Helper.ipynb 41
def add_example_to_docs(o: Any, example: str):
    """Add the given example to the object

    Args:
        o: an object, typically a function or a class, for which the example needs to be added
        example: The example string to add
    """

    original_doc = o.__doc__

    first_line, everything_else = original_doc.split("\n", 1)
    doc_with_example_added = (
        first_line
        + "\n"
        + textwrap.dedent(everything_else)
        + "\n"
        + textwrap.dedent(example)
    )

    o.__doc__ = doc_with_example_added
