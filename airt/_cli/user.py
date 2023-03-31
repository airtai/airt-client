# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/CLI_User.ipynb.

# %% auto 0
__all__ = ['logger']

# %% ../../notebooks/CLI_User.ipynb 3
from typing import *

# %% ../../notebooks/CLI_User.ipynb 4
import datetime as dt
import os

import pandas as pd
import qrcode
import typer
from tabulate import tabulate
from typer import echo

from airt._cli import helper
from airt._constant import SERVICE_PASSWORD
from airt._logger import get_logger, set_level
from airt.client import Client

# %% ../../notebooks/CLI_User.ipynb 6
app = typer.Typer(
    help="A set of commands for managing users and their authentication in the server."
)

# %% ../../notebooks/CLI_User.ipynb 8
logger = get_logger(__name__)

# %% ../../notebooks/CLI_User.ipynb 16
@app.command()
@helper.display_formated_table
@helper.requires_auth_token
def details(
    user: Optional[str] = typer.Option(
        None,
        "--user",
        "-u",
        help="Account user_uuid/username to get details. If not passed, then the currently logged-in details will be returned.",
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
        help="Output user uuid only.",
    ),
) -> Dict["str", Union[pd.DataFrame, str]]:
    """Get user details

    Please do not pass the optional 'user' option unless you are a super user. Only a super user can view details for other users.
    """

    from airt.client import User

    df = pd.DataFrame(User.details(user=user), index=[0])[User.USER_COLS]

    return {"df": df}

# %% ../../notebooks/CLI_User.ipynb 22
@app.command()
@helper.display_formated_table
@helper.requires_totp()
@helper.requires_auth_token
def create(
    username: str = typer.Option(
        ...,
        "--username",
        "-un",
        help="The new user's username. The username must be unique or an exception will be thrown.",
    ),
    first_name: str = typer.Option(
        ...,
        "--first_name",
        "-fn",
        help="The new user's first name.",
    ),
    last_name: str = typer.Option(
        ...,
        "--last_name",
        "-ln",
        help="The new user's last name.",
    ),
    email: str = typer.Option(
        ...,
        "--email",
        "-e",
        help="The new user's email. The email must be unique or an exception will be thrown.",
    ),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        help="The new user's password.",
    ),
    subscription_type: str = typer.Option(
        ...,
        "--subscription_type",
        "-st",
        help="User subscription type. Currently, the API supports only the following subscription types **small**, **medium** and **large**.",
    ),
    super_user: bool = typer.Option(
        False,
        "--super_user",
        "-su",
        help="If set to **True**, then the new user will have super user privilages. If **None**, then the default value "
        "**False** will be used to create a non-super user.",
    ),
    phone_number: Optional[str] = typer.Option(
        None,
        "--phone_number",
        "-ph",
        help="Phone number to be added to the user account. The phone number should follow the pattern of the country "
        "code followed by your phone number. For example, 440123456789, +440123456789, 00440123456789, +44 0123456789,"
        "and (+44) 012 345 6789 are all valid formats for registering a UK phone number.",
    ),
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app. Please pass this optional argument only if you have activated the MFA for your account.",
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
        help="Output user uuid only.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> Dict["str", Union[pd.DataFrame, str]]:
    """Create a new user in the server."""

    from airt.client import User

    df = User.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        subscription_type=subscription_type,
        super_user=super_user,
        password=password,
        phone_number=phone_number,
        otp=otp,
    )

    df["created"] = helper.humanize_date(df["created"])

    return {"df": df}

# %% ../../notebooks/CLI_User.ipynb 25
@app.command()
@helper.display_formated_table
@helper.requires_auth_token
def ls(
    offset: int = typer.Option(
        0,
        "--offset",
        "-o",
        help="The number of users to offset at the beginning. If **None**, then the default value **0** will be used.",
    ),
    limit: int = typer.Option(
        100,
        "--limit",
        "-l",
        help="The maximum number of users to return from the server. If None, then the default value 100 will be used.",
    ),
    disabled: bool = typer.Option(
        False,
        "--disabled",
        help="If set to **True**, then only the deleted users will be returned. Else, the default value **False** will "
        "be used to return only the list of active users.",
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
        help="Output only user uuids separated by space",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> Dict["str", Union[pd.DataFrame, str]]:
    """Return the list of users available in the server."""

    from airt.client import User

    ux = User.ls(offset=offset, limit=limit, disabled=disabled)

    df = User.as_df(ux)

    df["created"] = helper.humanize_date(df["created"])

    return {"df": df}

# %% ../../notebooks/CLI_User.ipynb 29
@app.command()
@helper.display_formated_table
@helper.requires_totp()
@helper.requires_auth_token
def disable(
    users: List[str] = typer.Argument(
        ...,
        help="user_uuid/username to disabled.  To disable multiple users, please pass the uuids/names separated by space.",
    ),
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app. Please pass this optional argument only if you have activated the MFA for your account.",
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
        help="Output user uuid only.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> Dict["str", Union[pd.DataFrame, str]]:
    """Disable a user in the server."""

    from airt.client import User

    users = [user for user in users]
    #     formated_users = helper.separate_integers_and_strings(users)

    df = User.disable(user=users, otp=otp)  # type: ignore
    df["created"] = helper.humanize_date(df["created"])

    return {"df": df}

# %% ../../notebooks/CLI_User.ipynb 33
@app.command()
@helper.display_formated_table
@helper.requires_totp()
@helper.requires_auth_token
def enable(
    users: List[str] = typer.Argument(
        ...,
        help="user_uuid/username to enable. To enable multiple users, please pass the uuids/names separated by space.",
    ),
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app. Please pass this optional argument only if you have activated the MFA for your account.",
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
        help="Output user uuid only.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> Dict["str", Union[pd.DataFrame, str]]:
    """Enable a disabled user in the server."""

    from airt.client import User

    users = [user for user in users]
    #     formated_users = helper.separate_integers_and_strings(users)

    df = User.enable(user=users, otp=otp)  # type: ignore
    df["created"] = helper.humanize_date(df["created"])

    return {"df": df}

# %% ../../notebooks/CLI_User.ipynb 39
@app.command()
@helper.display_formated_table
@helper.requires_totp()
@helper.requires_auth_token
def update(
    user: Optional[str] = typer.Option(
        None,
        "--user",
        help="Account user_uuid/username to update. If not passed, then the default value None will be used to update the currently logged-in user details.",
    ),
    username: Optional[str] = typer.Option(
        None,
        "--username",
        "-un",
        help="New username for the user.",
    ),
    first_name: Optional[str] = typer.Option(
        None,
        "--first_name",
        "-fn",
        help="New first name for the user.",
    ),
    last_name: Optional[str] = typer.Option(
        None,
        "--last_name",
        "-ln",
        help="New last name for the user.",
    ),
    email: Optional[str] = typer.Option(
        None,
        "--email",
        "-e",
        help="New email for the user.",
    ),
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app. Please pass this optional argument only if you have activated the MFA for your account.",
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
        help="Output user uuid only.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
) -> Dict["str", Union[pd.DataFrame, str]]:
    """Update existing user details in the server.

    Please do not pass the optional user option unless you are a super user. Only a
    super user can update details for other users.

    """

    from airt.client import User

    df = User.update(
        user=user,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        otp=otp,
    )

    df["created"] = helper.humanize_date(df["created"])

    return {"df": df}

# %% ../../notebooks/CLI_User.ipynb 43
@app.command("register-phone-number")
@helper.requires_totp()
@helper.requires_auth_token
def register_phone_number(
    phone_number: Optional[str] = typer.Option(
        None,
        "--phone-number",
        "-p",
        help="""Phone number to register. The phone number should follow the pattern of the 
            country code followed by your phone number. For example, **440123456789, +440123456789,
            00440123456789, +44 0123456789, and (+44) 012 345 6789** are all valid formats for registering a UK phone number.
            If the phone number is not passed in the arguments, then the OTP will be sent to the phone 
            number that was already registered to the user's account.""",
    ),
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app. Please pass this optional argument only if you have activated the MFA for your account.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
):
    """Register and validate a phone number

    This is an interactive command, one called it will send an OTP via SMS to the phone number. Please enter the OTP you have received
    in the interactive prompt to complete the phone number registration process.

    After ten invalid OTP attempts, you have to call this command again to register the phone number.
    """

    from airt.client import User

    user = User.register_phone_number(phone_number=phone_number, otp=otp)

    while True:
        try:
            sms_otp = typer.prompt(
                f"We have sent a One-Time Password (OTP) to the phone number {user['phone_number']}. Please enter here"
            )
            typer.echo("\n")
            response = User.validate_phone_number(otp=sms_otp)
            typer.echo(
                f"The phone number {user['phone_number']} is successfully registered. We will send the OTP via SMS to this registered phone number when requested."
            )
            break
        except ValueError as e:
            typer.echo(e)
            if ("Too many failed attempts" in str(e)) or (
                "OTP entered is expired" in str(e)
            ):
                break

# %% ../../notebooks/CLI_User.ipynb 45
@app.command("reset-password")
def reset_password(
    username: Optional[str] = typer.Option(
        None, "--username", "-u", help="Account username to reset the password"
    ),
    new_password: Optional[str] = typer.Option(
        None, "--new-password", "-np", help="New password to set for the account"
    ),
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Set logger level to DEBUG and output everything.",
    ),
):
    """Reset the account password

    We currently support two types of OTPs to reset the password for your account and you don't have to be logged in to call this command

    \n\nThe command switches to interactive mode unless all arguments are passed. The interactive mode will prompt you for the missing details and ask you to choose a recovery option to reset your password. Currently, we only support resetting the password either using a TOTP or SMS OTP.
    \n\nIf you have already activated the MFA for your account, then you can either enter the dynamically generated six-digit verification code from the authenticator app (TOTP) or request an OTP via SMS to your registered phone number.
    \n\nIf the MFA is not activated already, then you can only request the OTP via SMS to your registered phone number.
    \n\nAfter selecting an option, please follow the on-screen instructions to reset your password. In case, you don't have MFA enabled or don't have access to your registered phone number, please contact your administrator.
    """

    from airt.client import User

    if username is None:
        username = typer.prompt("Please enter your username")

    if new_password is None:
        new_password = typer.prompt(
            "Please enter your new password", hide_input=True, confirmation_prompt=True
        )

    if otp is not None:
        try:
            status = User.reset_password(
                username=username, new_password=new_password, otp=otp
            )
            typer.echo(f"\n{status}")
            typer.echo(
                f"\nPlease don't forget to set the updated password in the `{SERVICE_PASSWORD}` environment variable"
            )
        except ValueError as e:
            typer.echo(e)
            raise typer.Exit(code=1)
    else:
        typer.echo("\nPlease choose an option to reset your password\n\n")

        while True:
            typer.echo(
                "[1] Reset password using the dynamically generated six-digit verification code from the authenticator application\n"
            )
            typer.echo(
                "[2] Reset password by requesting the OTP via SMS to the registered phone number\n"
            )
            typer.echo(
                "If you cannot access the authenticator application or your registered phone number, please contact your administrator.\n"
            )

            recovery_option = typer.prompt("Password reset option")

            if recovery_option in ["1", "2"]:
                break
            typer.echo("Please enter a valid password reset option")

        if recovery_option == "1":
            try:
                totp = typer.prompt(
                    "Please enter the OTP displayed in the authenticator application"
                )
                status = User.reset_password(
                    username=username, new_password=new_password, otp=totp
                )
            except ValueError as e:
                typer.echo(e)

        elif recovery_option == "2":
            try:
                sms_status = User.send_sms_otp(
                    username=username, message_template_name="reset_password"
                )
                typer.echo(f"\n{sms_status}\n")
                sms_otp = typer.prompt(
                    f"Please enter the One-Time Password (OTP) you received on your registered phone number"
                )
                status = User.reset_password(
                    username=username, new_password=new_password, otp=sms_otp
                )
            except ValueError as e:
                typer.echo(e)

        else:
            raise typer.Exit(code=1)

        typer.echo(f"\n{status}")

        if os.environ.get(SERVICE_PASSWORD) is not None:
            typer.echo(
                f"\nPlease don't forget to set the updated password in the `{SERVICE_PASSWORD}` environment variable"
            )

# %% ../../notebooks/CLI_User.ipynb 48
mfa_app = typer.Typer(
    help="Commands for enabling and disabling Multi-Factor Authentication (MFA)."
)

# %% ../../notebooks/CLI_User.ipynb 49
@mfa_app.command()  # type: ignore
@helper.requires_totp()
@helper.requires_auth_token
def enable(
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app. Please pass this optional argument only if you have activated the MFA for your account.",
    ),
) -> None:
    """Enable Multi-Factor Authentication (MFA) for the user.

    This is an interactive command and will generate a QR code. You can use an authenticator app, such as Google Authenticator
    to scan the code and enter the valid six-digit verification code from the authenticator app in the interactive prompt to
    enable and activate MFA for your account.

    After three invalid attempts, you have to call this command again to generate a new QR code.
    """

    from airt.client import User

    qr = qrcode.QRCode()
    qr.add_data(User._get_mfa_provision_url(otp=otp))

    typer.echo("Please open an authenticator app and scan the QR code below:")
    #     typer.echo(qr.print_ascii(invert=True))
    typer.echo(qr.print_ascii())

    for i in range(3):
        try:
            activation_otp = typer.prompt(
                "Please enter the OTP displayed in the authenticator app"
            )
            response = User.activate_mfa(otp=activation_otp)
            typer.echo("Multi-Factor Authentication (MFA) successfully activated.")

            details = User.details()
            status = helper.get_phone_registration_status(details)
            if status is not None:
                typer.echo(status)

            break

        except ValueError as e:
            typer.echo(e)

# %% ../../notebooks/CLI_User.ipynb 51
@mfa_app.command()  # type: ignore
@helper.requires_totp_or_otp(message_template_name="disable_mfa")
@helper.requires_auth_token
def disable(
    user: Optional[str] = typer.Option(
        None,
        "--user",
        "-u",
        help="Account user_uuid/username to disable MFA. If not passed, then the default value None will be used to disable MFA for the currently logged-in user.",
    ),
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app or the OTP you have received via SMS.",
    ),
) -> None:
    """Disable Multi-Factor Authentication (MFA) for the user.

    The command switches to interactive mode unless the OTP argument is passed. The interactive mode will prompt you to
    choose an OTP option you want to use. Currently, we only support disabling MFA either using a TOTP or SMS OTP.

    If you have access to the authenticator application, then you can either enter the dynamically generated six-digit
    verification code from the authenticator app (TOTP) or request an OTP via SMS to your registered phone number.

    After selecting an option, please follow the on-screen instructions to disable MFA for your account. In case,
    you don't have access to the authenticator app and your registered phone number, please contact your administrator.

    Note: Please do not pass the user argument unless you are a super user. Only
    a super user can disable MFA for other users.
    """

    from airt.client import User

    User.disable_mfa(user=user, otp=otp)

    typer.echo(
        "Multi-Factor Authentication (MFA) is successfully deactivated for the user."
    )

# %% ../../notebooks/CLI_User.ipynb 55
# Adding mfa as a subcommand for user command
app.add_typer(mfa_app, name="mfa")

# %% ../../notebooks/CLI_User.ipynb 57
sso_app = typer.Typer(help="Commands for enabling and disabling Single sign-on (SSO).")

# %% ../../notebooks/CLI_User.ipynb 58
@sso_app.command()  # type: ignore
@helper.requires_totp()
@helper.requires_auth_token
def disable(
    sso_provider: str = typer.Argument(
        ...,
        help="Name of the Single sign-on (SSO) identity provider. At present, the API only supports Google and Github as valid SSO identity providers.",
    ),
    user: Optional[str] = typer.Option(
        None,
        "--user",
        "-u",
        help="Account user_uuid/username to disable MFA. If not passed, then the default value None will be used to disable SSO for the currently logged-in user.",
    ),
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app. Please pass this optional argument only if you have activated the MFA for your account.",
    ),
) -> None:
    """Disable Single sign-on (SSO) for the user.

    Please do not pass the user argument unless you are a super user. Only
    a super user can disable SSO for other users.
    """

    from airt.client import User

    success_msg = User.disable_sso(sso_provider=sso_provider, user=user, otp=otp)
    typer.echo(success_msg)

# %% ../../notebooks/CLI_User.ipynb 60
@sso_app.command()  # type: ignore
@helper.requires_totp()
@helper.requires_auth_token
def enable(
    sso_provider: str = typer.Argument(
        ...,
        help="Name of the Single sign-on (SSO) identity provider. At present, the API only supports **Google** and **Github** as valid SSO identity providers.",
    ),
    sso_email: str = typer.Option(
        ...,
        "--email",
        "-e",
        help="Email id going to be used for SSO authentication.",
    ),
    otp: Optional[str] = typer.Option(
        None,
        "--otp",
        help="Dynamically generated six-digit verification code from the authenticator app. Please pass this optional argument only if you have activated the MFA for your account.",
    ),
) -> None:
    """Enable Single sign-on (SSO) for the user"""

    from airt.client import User

    success_msg = User.enable_sso(
        sso_provider=sso_provider, sso_email=sso_email, otp=otp
    )

    typer.echo(success_msg)

# %% ../../notebooks/CLI_User.ipynb 63
# Adding sso as a subcommand for user command
app.add_typer(sso_app, name="sso")
