# auth.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from flask import request, session
from .utils import DatabaseContext
from .accounts import get_account, get_account_by_github_id, create_account
from passlib.hash import pbkdf2_sha256
from requests import get, post, Response

def authenticate_with_github(temporary_code, **kwargs) -> str:
    """Attempt to authenticate with GitHub using the temporary code."""
    if "client_id" not in kwargs or "client_secret" not in kwargs:
        raise PermissionError("Cannot authenticate to GitHub with empty client information.")
    
    gh_api_response: Response = post("https://github.com/login/oauth/access_token",
        params={
            "client_id": kwargs["client_id"],
            "client_secret": kwargs["client_secret"],
            "code": temporary_code,
        },
        headers={"Accept": "application/json"} )

    gh_api_response.raise_for_status()
    gh_access_token = gh_api_response.json()["access_token"]

    gh_data_response = get("https://api.github.com/user", headers={"Authorization": f"token {gh_access_token}"})
    gh_data_response.raise_for_status()

    gh_acct_data = gh_data_response.json()
    gh_email, gh_id, gh_name = gh_acct_data["email"], gh_acct_data["id"], (gh_acct_data["name"] or gh_acct_data["login"])

    # Get the account from the database, assuming it exists.
    register_on = False
    account = get_account_by_github_id(kwargs["app_database"], gh_id)

    # If the account doesn't exist, assume that the user wants to register for the first time.
    if not account:
        register_on = True
        account = create_account(kwargs["app_database"], gh_name, gh_email, gh_id)
        session["rxw_reg"] = True

    # Otherwise, assume that the user is logging in. Set the token accordingly.
    session["cuid"] = account["userid"]
    session["login_token"] = auth_token(0, account["email"], account["githubid"], account["name"])
    session.modified = True

    return "registered" if register_on else "returned"




def authenticated(with_app_db) -> bool:
    """Returns whether the user is authenticated."""

    # Check that we have stored a token and current user ID in the session storage.
    token, cuid = session.get("login_token"), session.get("cuid")
    if not token or not cuid:
        return False

    # Fetch the user data from the database. If this user doesn't exist, return false.
    user_account = get_account(with_app_db, cuid)
    if not user_account:
        return False

    # Compare the user data to the token in the session storage.
    email, name, github_id = user_account["email"], user_account["name"], user_account["githubid"]
    return pbkdf2_sha256.verify(token, auth_token(cuid, email, github_id, name))



def auth_token(user_id, user_email, gh_id, user_name) -> str:
    """Returns an authentication token based on the format of the DB."""
    return pbkdf2_sha256.hash(f"{user_id}:{user_email}:{gh_id}:{user_name}")
