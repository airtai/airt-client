# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/API_Keys.ipynb.

# %% auto 0
__all__ = ['APIKey']

# %% ../../notebooks/API_Keys.ipynb 4
from typing import *

# %% ../../notebooks/API_Keys.ipynb 5
import os

from datetime import datetime, timedelta, date

import pandas as pd
from fastcore.foundation import patch

from airt.components.client import Client
from airt.components.user import User
from airt.logger import get_logger, set_level
from airt.helper import (
    get_data,
    post_data,
    delete_data,
    generate_df,
    get_attributes_from_instances,
    check_and_append_otp_query_param,
)

# %% ../../notebooks/API_Keys.ipynb 7
logger = get_logger(__name__)

# %% ../../notebooks/API_Keys.ipynb 11
class APIKey:
    """A class for managing the APIKeys in the server.

    Both the APIKey and the token can be used for accessing the airt services. However, there is a slight difference in generating and managing the two.

    For generating the APIKey, you first need to get the developer token. Please refer to `Client.get_token` method documentation to generate one.

    After logging in with your developer token, you can create any number of new APIKeys and can set an expiration date individually. You can also access
    other methods available in the APIKey class to list, revoke the APIKey at any time.

    Here's an example of how to use the APIKey class to create a new key and use it to access the airt service.

    Example:
        ```python
        # Importing necessary libraries
        from  airt.client import Client, APIKey, User

        # Authenticate
        Client.get_token(username="{fill in username}", password="{fill in password}")

        # Create a new key with the given name
        key_name = "{fill in key_name}"
        new_key = APIKey.create(name=key_name)

        # Display the details of the newly created key
        print(APIKey.details(apikey=key_name))

        # Call the set_token method to set the newly generated key
        Client.set_token(token=new_key["access_token"])

        # Print the logged-in user details
        # If set_token fails, the line below will throw an error.
        print(User.details())
        ```
    """

    API_KEY_COLS = ["uuid", "name", "created", "expiry", "disabled"]

    def __init__(
        self,
        uuid: str,
        name: Optional[str] = None,
        expiry: Optional[str] = None,
        disabled: Optional[bool] = None,
        created: Optional[str] = None,
    ):
        """Constructs a new APIKey instance.

        Args:
            uuid: APIKey uuid.
            name: APIKey name.
            expiry: APIKey expiry date.
            disabled: Flag to indicate the status of the APIKey.
            created: APIKey creation date.
        """
        self.uuid = uuid
        self.name = name
        self.expiry = expiry
        self.disabled = disabled
        self.created = created

    @staticmethod
    def create(
        name: str,
        expiry: Optional[Union[int, timedelta, datetime]] = None,
        otp: Optional[str] = None,
    ) -> Dict[str, str]:
        """Create a new APIKey

        In order to access the airt service with the newly generated APIKey, please call the `Client.set_token` method
        or set the APIKey value in the **AIRT_SERVICE_TOKEN** environment variable.

        !!! note

            - The APIKey's name must be unique. If not, an exception will be raised while creating a new key with the name of an existing key.
            However, you can create a new key with the name of a revoked key.

            - The expiry for an APIKey is optional, if not passed then the default value **None** will be used to create an APIKey with no expiry date!

        Args:
            name: The name of the APIKey.
            expiry: The validity for the APIKey. This can be an integer representing the number of days till expiry, can be
                an instance of timedelta (timedelta(days=x)) or can be an instance of datetime. If not passed, then the default value
                **None** will be used to create a APIKey that will never expire!
            otp: Dynamically generated six-digit verification code from the authenticator app. Please pass this
                parameter only if the MFA is enabled for your account.

        Returns:
            The APIKey and its type as a dictionary.

        Raises:
            ValueError: If the user is not authenticated.
            ValueError: If the user tries to create a new APIKey with an existing key name.
            ValueError: If the OTP is invalid.
            ConnectionError: If the server address is invalid or not reachable.

        In the following example, a new APIKey is created with a 10-day expiration date and used to access the airt service.

        Example:
            ```python
            # Importing necessary libraries
            from  airt.client import Client, APIKey

            # Authenticate
            Client.get_token(username="{fill in username}", password="{fill in password}")

            # Create a key with the given name and set the expiry to 10 days from now.
            # If the expiry parameter is not specified, a key with no expiry date is created.
            key_name = "{fill in key_name}"
            new_key_details = APIKey.create(name=key_name, expiry=10)

            # Display the details of the newly created key
            print(APIKey.details(apikey=key_name))

            # If a new key with the same name is created, an exception will be raised.
            # However, you can create a new key with the name of a revoked key.
            try:
                APIKey.create(name=key_name, expiry=10)
                print("Should not print this, the above line should raise an exception")
                raise RuntimeException()

            except ValueError as e:
                print("Expected to fail, everything is fine")

            # Finally, either call the below method to set the newly generated key
            # or store it in the AIRT_SERVICE_TOKEN environment variable.
            Client.set_token(token=new_key_details["access_token"])

            # If set_token fails, the line below will throw an error.
            print(APIKey.details(apikey=key_name))
            ```
        """
        if expiry is None:
            expiry_date = expiry
        else:
            if isinstance(expiry, int):
                delta = datetime.now() + timedelta(days=expiry)
            elif isinstance(expiry, timedelta):
                delta = datetime.now() + expiry
            else:
                delta = expiry

            expiry_date = delta.strftime("%Y-%m-%dT%H:%M")

        return Client._post_data(
            relative_url="/apikey",
            json=dict(name=name, expiry=expiry_date, otp=otp),
        )

    @staticmethod
    def as_df(ax: List["APIKey"]) -> pd.DataFrame:
        """Return the details of APIKey instances in a pandas dataframe.

        Args:
            ax: List of APIKey instances.

        Returns:
            Details of all the APIKeys in a dataframe.

        Raises:
            ConnectionError: If the server address is invalid or not reachable.

        An example of displaying the APIKeys generated by the currently logged-in user in a dataframe

        Example:
            ```python
            # Importing necessary libraries
            from  airt.client import Client, APIKey

            # Authenticate
            Client.get_token(username="{fill in username}", password="{fill in password}")

            # Create a key without an expiry date in the given name
            key_name = "{fill in key_name}"
            APIKey.create(name=key_name)

            # Display all the APIKey instance details in a pandas dataframe
            df = APIKey.as_df(APIKey.ls())
            print(df)
            ```
        """
        lists = get_attributes_from_instances(ax, APIKey.API_KEY_COLS)  # type: ignore
        return generate_df(lists, APIKey.API_KEY_COLS)

    @staticmethod
    def ls(
        user: Optional[str] = None,
        offset: int = 0,
        limit: int = 100,
        include_disabled: bool = False,
    ) -> List["APIKey"]:
        """Return the list of APIKeys instances.

        Please do not pass the **user** parameter unless you are a super user. Only a super user can view
        the APIKeys created by other users.

        Args:
            user: user_uuid/username associated with the APIKey. Please call `User.details` method of the User class to get your user_uuid.
                If not passed, then the currently logged-in user_uuid will be used.
            offset: The number of APIKeys to offset at the beginning. If None, then the default value 0 will be used.
            limit: The maximum number of APIKeys to return from the server. If None, then the default value 100 will be used.
            include_disabled: If set to **True**, then the disabled APIKeys will also be included in the result.

        Returns:
            A list of APIKey instances.

        Raises:
            ConnectionError: If the server address is invalid or not reachable.
            ValueError: If the user_uuid is invalid.

        An example of displaying the APIKeys generated by the currently logged-in user

        Example:
            ```python
            # Importing necessary libraries
            from  airt.client import Client, APIKey

            # Authenticate
            Client.get_token(username="{fill in username}", password="{fill in password}")

            # Create a key without an expiry date in the given name
            key_name = "{fill in key_name}"
            APIKey.create(name=key_name)

            # Get the list of all APIKey instances created by the currently logged-in user.
            # If you are a super user, you can view the APIkeys created by other users by
            # passing their uuid/username in the user parameter.
            ax = APIKey.ls()
            print(ax)

            # Display the details of the instances in a pandas dataframe
            df = APIKey.as_df(ax)
            print(df)
            ```
        """
        user_uuid = User.details(user=user)["uuid"]

        apikeys = Client._get_data(
            relative_url=f"/{user_uuid}/apikey?include_disabled={include_disabled}&offset={offset}&limit={limit}"
        )

        ax = [
            APIKey(
                uuid=apikey["uuid"],
                name=apikey["name"],
                expiry=apikey["expiry"],
                disabled=apikey["disabled"],
                created=apikey["created"],
            )
            for apikey in apikeys
        ]

        return ax

    @staticmethod
    def details(apikey: str) -> pd.DataFrame:
        """Return details of an APIKey.

        Args:
            apikey: APIKey uuid/name.

        Returns:
            A pandas Dataframe encapsulating the details of the APIKey.

        Raises:
            ValueError: If the APIKey uuid is invalid.
            ConnectionError: If the server address is invalid or not reachable.

        An example to get details of an APIKey

        Example:
            ```python
            # Importing necessary libraries
            from  airt.client import Client, APIKey

            # Authenticate
            Client.get_token(username="{fill in username}", password="{fill in password}")

            # Create a key without an expiry date in the given name
            key_name = "{fill in key_name}"
            APIKey.create(name=key_name)

            # Display the details of the newly created key
            print(APIKey.details(apikey=key_name))

            # To display the details of all keys created by the user, use the method below.
            df = APIKey.as_df(APIKey.ls())
            print(df)
            ```
        """
        details = Client._get_data(relative_url=f"/apikey/{apikey}")

        return pd.DataFrame(details, index=[0])[APIKey.API_KEY_COLS]

    @staticmethod
    def _get_key_names(keys: Union[List["APIKey"], List[str], str]) -> List[str]:
        """Get keys names

        Args:
            keys: Can be a string, list of string or a list of APIKey instances

        Returns:
            The APIKey names as a list
        """
        if isinstance(keys, str):
            return [keys]

        if all(isinstance(k, str) for k in keys):
            return keys  # type: ignore

        return [k.name for k in keys]  # type: ignore

    @staticmethod
    def revoke(
        keys: Union[str, List[str], List["APIKey"]],
        user: Optional[str] = None,
        otp: Optional[str] = None,
    ) -> pd.DataFrame:
        """Revoke one or more APIKeys

        Please do not pass the **user** parameter unless you are a super user. Only a super user can revoke the
        APIKeys created by other users.

        Args:
            keys: APIKey uuid/name to revoke. To revoke multiple keys, either pass a list of APIKey uuid/names or a list of APIKey instances.
            user: user_uuid/username associated with the APIKey. Please call `User.details` method of the User class to get your user_uuid/username.
                If not passed, then the currently logged-in user will be used.
            otp: Dynamically generated six-digit verification code from the authenticator app. Please pass this
                parameter only if the MFA is enabled for your account.

        Returns:
             A pandas Dataframe encapsulating the details of the deleted APIKey(s).

        Raises:
            ValueError: If the APIKey uuid is invalid.
            ValueError: If the user_uuid is invalid.
            ValueError: If the OTP is invalid.
            ConnectionError: If the server address is invalid or not reachable.

        An example to revoke a single APIKey by name

        Example:
            ```python
            # Importing necessary libraries
            from  airt.client import Client, APIKey

            # Authenticate
            Client.get_token(username="{fill in username}", password="{fill in password}")

            # Create a key without an expiry date in the given name
            key_name = "{fill in key_name}"
            APIKey.create(name=key_name)

            # Check that the newly created key exists
            print([key.name for key in APIKey.ls()])

            # Revoke the newly created key
            # To delete multiple keys, pass a list of key names or key instances
            APIKey.revoke(keys=key_name)

            # Check that the newly created key does not exists
            print([key.name for key in APIKey.ls()])
            ```

        Here's an example of a super user revoking all APIkeys generated by a specific user.

        Example:
            ```python
            # Importing necessary libraries
            from  airt.client import Client, APIKey

            # Authenticate with super user privileges
            Client.get_token(
                username="{fill in super_user_username}",
                password="{fill in super_user_password}"
            )

            # List the APIKeys generated by a specific user
            user = "{fill in other_username}"
            ax = APIKey.ls(user=user)
            print([key.name for key in ax])

            # Revoke the APIKeys
            APIKey.revoke(keys=ax, user=user)

            # Check that all APIkeys have been revoked
            print([key.name for key in APIKey.ls(user=user)])
            ```
        """
        user_uuid = User.details(user=user)["uuid"]
        _keys = APIKey._get_key_names(keys)

        response_list = []

        for key_uuid in _keys:
            url = f"/{user_uuid}/apikey/{key_uuid}"
            response = Client._delete_data(
                relative_url=check_and_append_otp_query_param(url, otp)
            )
            response_list.append(response)

        return generate_df(response_list, APIKey.API_KEY_COLS)
